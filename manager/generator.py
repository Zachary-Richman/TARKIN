import hashlib
import config
import numpy as np


def solve_for_semi_major_axis(a_i, m_i, m_j, spacing, m_star) -> float:
    """

    :param a_i: Semi-major axis of the n - 1 planet
    :param m_i: Mass of the n - 1 planet
    :param m_j: Mass of the current planet
    :param spacing: spacing in mutual hill radii
    :param m_star: mass of the central star
    :return: the value of a_j
    """
    k: float = spacing * np.cbrt(
        (m_i + m_j) / (3 * m_star)
    )

    return a_i * (2 + k) / (2 - k)

def solve_for_eccentricity_max(a_i, a_j) -> float:
    return (a_j - a_i) / (a_i + a_j)


class GenerateSystem:
    def __init__(self, system_id):
        if not 1 <= system_id <= 105_000:
            raise ValueError("system_id must be between 1 and 105000")

        self.system_id = system_id  # run #, 1 ... 120,000
        self.seed = self.derive_seed()
        self.rng = np.random.default_rng(self.seed)

        self.n_planets = (
            (system_id - 1) // config.sys_per_n_value
        ) + config.min_planets

        self.planets = [
            {
                "name": f"{i + 1}",
                "mass": None,  # kg
                "a": None,  # m; semimajor axis
                "e": None,  # dimensionless
                "inc": None,  # radians
                "Omega": None,  # radians
                "omega": None,  # radians
                "M": None,  # radians
            }
            for i in range(self.n_planets)
        ]

        self.perturber = {
            "name": "The Sovereign",
            "mass": 0.0,  # kg
            "a": 0.0,  # m
            "e": 0.0,
            "inc": 0.0,  # radians
            "Omega": 0.0,  # radians
            "omega": 0.0,  # radians
            "M": 0.0,  # radians
        }

    def derive_seed(self):
        key = f"TARKIN_v1_{self.system_id}" # unique id beyond just the number
        digest = hashlib.sha256(key.encode("utf-8")).digest()
        return int.from_bytes(digest, byteorder="big")  # big endian

    def _generate_masses(self) -> None:
        for planet in self.planets:
            planet["mass"] = float(
                self.rng.uniform(
                    config.m_planet_min,
                    config.m_planet_max,
                )
            )

    def _generate_semimajor_axes(self):
        # Fix the innermost planet's orbit
        self.planets[0]["a"] = config.innermost_a

        for j in range(1, self.n_planets):
            inner = self.planets[j - 1]
            outer = self.planets[j]

            spacing = float(
                self.rng.uniform(
                    8,
                    20,
                )
            )

            outer["a"] = solve_for_semi_major_axis(
                inner["a"],
                inner["mass"],
                outer["mass"],
                spacing,
                config.m_sun,
            )

    def _generate_eccentricities(self):
        print("system_id:", self.system_id)
        print("n_planets:", self.n_planets)
        print("len(planets):", len(self.planets))

        e_max_system = min(  # find the lowest possible max_e across all adjacent pairs
            solve_for_eccentricity_max(
                self.planets[i]["a"],
                self.planets[i + 1]["a"],
            )
            for i in range(self.n_planets - 1)
        )

        # Sample each planet's eccentricity below the system-wide ceiling.
        for planet in self.planets:
            planet["e"] = float(
                self.rng.uniform(0.0, e_max_system)
            )

    def _generate_inclination(self):
        for planet in self.planets:
            planet["inc"] = 0.0

    def _generate_longitude_ascending_node(self):
        for planet in self.planets:
            planet["Omega"] = 0.0

    def _generate_argument_of_periapsis(self):
        for planet in self.planets:
            planet["omega"] = float(self.rng.uniform(
                0,
                2 * np.pi
            ))

    def _generate_mean_anomaly(self):
        for planet in self.planets:
            planet["M"] = self.rng.uniform(
                0,
                2 * np.pi
            )

    def _generate_perturber(self):
        # to overwrite pregenerated figures with the defined params from the paper
        self.perturber["mass"] = config.m_perturber

        self.perturber["a"] = (
                self.planets[-1]["a"]
                + config.a_additional_perturber
        )

        self.perturber["M"] = float(
            self.rng.uniform(0.0, 2.0 * np.pi)
        )
        # all other values are set to 0.0, not as a default value
        # but to mimic the params demonstrated in all other planets


        # This is making a critical conceit for the sake of investigation,
        # We will not be modifying any other pieces of the perturber as
        # it will undermine the presence at a distance/greater mass
        # and will have greater influence on initial rotational/positional params
        # holding eccentricity/inclination fixed controls any additional sources of variation
        # certainly a limitation, to be addressed at a later point perhaps (not in the EE)

    def run(self) -> dict:
        self._generate_masses()
        self._generate_semimajor_axes()
        self._generate_eccentricities()
        self._generate_inclination()
        self._generate_longitude_ascending_node()
        self._generate_argument_of_periapsis()
        self._generate_mean_anomaly()

        self._generate_perturber()

        return {
            "system_id": self.system_id,
            "seed": self.seed,
            "planets": self.planets,
            "perturber": self.perturber,
        }