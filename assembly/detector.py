"""
assembly/detector.py
====================
Instability event instance detection

Detector (class) works with a snapshot-based instability checking system.
It does NOT integrate, that is purely the simulation runners function
Each call to Detector.check() reads the current simulation and returns either:
UnstableDetection | None

Detection Hierarchy (priority order):
1. Inner-Planet Close Encounters: distance(i, j) < R_mH(i, j)
2. Outer-Planet Close Encounters: distance(i, og) > R_mH(i, og)
3. High Eccentricity: e_i > 0.9
4. Stellar Collision: a_i(1 - e_i) < 0.01
5. Ejection: a_i > 100AU or orbit() failure

The mutual Hill radius between planets i and j (Gladman 1993 [1]):
    R_mH = ((a_i + a_j) / 2) * ((m_i + m_j) / (3 * M_star))^(1/3)

Mutual Hill Radii are computed once at initialization (at t=0) and are never changed.
Near (or at) instability the radii will change (mass and semi-major axis remain constant), therefore it is not necessary to recompute the Hill Radius each .check() call


NOTE: TARKIN uses sim.ri_whfast.safe_mode = 0 (REBOUND, Rein, et al. [2])
    if it was set to the default (1) WHFast would recalculate all the internal coordinates (Jacobi, heliocentric, WHDS, barycentric) and
     synchronize all every timestep, as such, to increase speed this is disabled.
    Unconditionally, before any work is done by the checker it reconciles the internal coordinates
    Any caller that bypasses check() and reads particle state directly MUST call sim.ri_whfast.integrator_synchronize() first.

References:
[1] Gladman 1993
    https://doi.org/10.1006/icar.1993.1168
[2] Rein, H. et al. REBOUND N-body integrator (v4.6.0)
    GitHub: https://github.com/hannorein/rebound
    Documentation: https://rebound.hanno-rein.de/integrators/
    Accessed: March 2026
"""
import rebound
from core import constants as const
from assembly.dataclasses_.detector_dataclass import UnstableDetection


class Detector:
    def __init__(self, sim: rebound.Simulation):
        self.sim = sim
        self.has_outer_giant = self._check_has_outer_giant()
        self.hill_radii = self._generate_static_hill_radii()

    def _check_has_outer_giant(self) -> bool:
        try:
            _ = self.sim.particles["outer_giant"]
            return True
        except rebound.ParticleNotFound:
            return False

    def _generate_static_hill_radii(self) -> dict:  # [1]
        """
        Compute mutual Hill radii for all non-star particle pairs.

        Call this ONCE before the integration loop and pass the result
        into every check() call. Hill radii are stable enough during
        a well-behaved integration that recomputing every step is wasteful.

        Near instability, the mH will drift, this is acceptable for a
        statistical study and is noted as a simplification in the methods.

        Mutual Hill radius between planets i and j:
            R_mH = ((a_i + a_j) / 2) * ((m_i + m_j) / (3 * M_star))^(1/3) [1]
        :param sim: rebound.Simulation object
        :return: dict of mutual Hill radii pairs
        """
        star = self.sim.particles[0]
        indices = list(range(1, self.sim.N))  # all non-star particle indices

        hill_radii = {}  # return object

        for i in indices:
            for j in indices:
                if j <= i: continue

                particle_i = self.sim.particles[i]
                particle_j = self.sim.particles[j]

                semi_major_axis_i = particle_i.orbit(primary=star).a
                semi_major_axis_j = particle_j.orbit(primary=star).a

                semi_major_axis_avg = (semi_major_axis_i + semi_major_axis_j) / 2
                mass_sum = particle_i.m + particle_j.m

                R_mH = semi_major_axis_avg * (
                               mass_sum / (3 * star.m)
                       ) ** (1 / 3)

                hill_radii[(  # take it by min, max, so we can know how to access it later
                    min(i, j),
                    max(i, j)
                )] = R_mH

        return hill_radii

    @staticmethod
    def _distance(a, b):
        d_x = abs(a.x - b.x)
        d_y = abs(a.y - b.y)
        d_z = abs(a.z - b.z)

        return (
            d_x ** 2 + d_y ** 2 + d_z ** 2
        ) ** (1/2)

    def check(self) -> UnstableDetection | None:
        """
        Check a simulation snapshot for instability events.

        Runs four checks in the following order (priority):
        1. Inner planet close encounters (R_mH)
        2. Outer planet close encounters (R_mH)
        3. High eccentricity (safety catch for potentially missed encounters)
        4. Collision or ejection (safety catch for potentially missed encounters)

        :return: UnstableDetection instance or None if no instability events
        """
        sim = self.sim

        # since safe_mode = 0, REBOUND doesn't sync the Jacobi coords to inertial after each step
        # therefore distance calculations are wrong, but the fix is simple [2]:
        self.sim.integrator_synchronize()

        star = sim.particles[0]
        outer_planet = None

        if self.has_outer_giant:
            try:
                outer_planet = sim.particles["outer_giant"]
            except rebound.ParticleNotFound:
                pass

        inner_planets = [
            p for p in sim.particles
            if p.index != star.index
               and (outer_planet is None or p.index != outer_planet.index)
        ]

        # check inners
        for idx_i, planet_i in enumerate(inner_planets):
            for idx_j, planet_j in enumerate(inner_planets):
                if idx_i <= idx_j: continue

                d = self._distance(planet_i, planet_j)
                R_mH = self.hill_radii[(  # getting min/max as to guarantee getting the right object
                    min(planet_i.index, planet_j.index),
                    max(planet_i.index, planet_j.index)
                )]

                if d < R_mH:
                    return UnstableDetection(
                        event_type="close_encounter_inner",
                        time=sim.t,
                        body=str(planet_i.hash),
                        value=d,
                        threshold=R_mH
                    )

        # check outers (2)
        if outer_planet is not None:
            for planet_i in inner_planets:
                d = self._distance(planet_i, outer_planet)
                R_mH = self.hill_radii[(  # getting min/max as to guarantee getting the right object
                    min(planet_i.index, outer_planet.index),
                    max(outer_planet.index, outer_planet.index)
                )]

                if d < R_mH:
                    return UnstableDetection(
                        event_type="close_encounter_outer",
                        time=sim.t,
                        body=str(planet_i.hash),
                        value=d,
                        threshold=R_mH
                    )

        # check failsafe (3 & 4)
        for planet in inner_planets:
            try:
                orb = planet.orbit(primary=star)
            except Exception:
                # orbit can fail if the particle escaped, treat as ejection
                return UnstableDetection(
                    event_type="ejection",
                    time=sim.t,
                    body=str(planet.hash),  # else returns a c_unit
                    value=float("nan"),
                    threshold=const.MAX_SEPARATION
                )

            if orb.e > const.MAX_ECCENTRICITY:
                return UnstableDetection(
                    event_type="high_eccentricity",
                    time=sim.t,
                    body=str(planet.hash),
                    value=orb.e,
                    threshold=const.MAX_ECCENTRICITY
                )

            periapsis = orb.a * (1 - orb.e)  # distance to the center  = semi-major-axis * eccentricity
            if periapsis < const.MIN_PERIAPSIS:
                return UnstableDetection(
                    event_type="stellar_collision",
                    time=sim.t,
                    body=str(planet.hash),
                    value=periapsis,
                    threshold=const.MIN_PERIAPSIS
                )

            # if a is over max separation then likely ejection
            if orb.a > const.MAX_SEPARATION:
                return UnstableDetection(
                    event_type="ejection",
                    time=sim.t,
                    body=str(planet.hash),
                    value=orb.a,
                    threshold=const.MAX_SEPARATION
                )

        return None # all checks passed, system is stable :)