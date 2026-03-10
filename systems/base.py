import rebound
from tabulate import tabulate # used for the summary function
import numpy as np
import copy

class BaseSystem:
    name = "BaseSystem"
    planets = []
    star_mass = 1.0

    def __init__(self, seed: int, outer_giant: dict | None = None):
        self.seed: int = seed
        self.outer_giant: dict | None = outer_giant
        self._rng = np.random.default_rng(seed)
        self.sim = rebound.Simulation()


    def build(self):
        working_planets = copy.deepcopy(self.planets)

        self.sim.add(m=self.star_mass, hash="star")  # adding the star

        # add in the planets
        for planet in working_planets:
            self._fill_defaults(planet)
            self.sim.add(
                m = planet["m"],
                a = planet["a"],
                e = planet["e"],
                inc = planet["inc"],
                Omega = planet["Omega"],
                omega = planet["omega"],
                f = planet["f"],
                hash = planet["name"],
            )

        # add outer giant
        if self.outer_giant is not None:
            og = copy.deepcopy(self.outer_giant)
            self._fill_defaults(og)
            self.sim.add(
                m = og["m"],
                a = og["a"],
                e = og["e"],
                inc = og["inc"],
                Omega = og["Omega"],
                omega = og["omega"],
                f = og["f"],
                hash = "outer_giant",
            )

        self.sim.move_to_com()  # stability, keeps in frame
        return self.sim

    def _fill_defaults(self, planet: dict):
        """
        variables:
        * = required
        *a (distance) -> already defined
        *m (mass) -> already defined
        e (eccentricity) -> constant (0.0) - float
        inc (inclination) -> [0, 2pi) - radians
        Omega (longitude of ascending node) -> [0, 2pi) - radians
        omega (periapsis) -> [0, 2pi) - radians
        f (true anomaly, starting pos) -> [0, 2pi) - radians
        """
        E_DEFAULT: float = 0.0
        INC_MAX = 0.05
        TWO_PI = 2 * np.pi

        for field in ("m", "a"):
            if field not in planet:
                raise KeyError(f"field {field} is not defined in planet: {planet}")

        planet.setdefault("name", "unnamed")
        planet.setdefault("e", E_DEFAULT)
        planet.setdefault("inc", float(self._rng.uniform(0.0, INC_MAX)))
        planet.setdefault("Omega", float(self._rng.uniform(0.0, TWO_PI)))
        planet.setdefault("omega", float(self._rng.uniform(0.0, TWO_PI)))
        planet.setdefault("f", float(self._rng.uniform(0.0, TWO_PI)))

        return planet

    def summary(self):
        headers = ["name", "mass", "axis separation", "eccentricity",
                   "inclination", "longitude of ascending node", "periapsis", "true anomaly"]

        working = copy.deepcopy(self.planets)
        for planet in working:
            self._fill_defaults(planet)

        rows = [[
            planet["name"],
            planet["m"],
            planet["a"],
            planet["e"],
            planet["inc"],
            planet["Omega"],
            planet["omega"],
            planet["f"]
        ] for planet in working]

        print(f"Summary Table of System: {self.name}")
        print("-" * 50)
        print(tabulate(rows, headers, tablefmt="plain"))
