"""
systems/kepler11.py
====================

Source:
    Lissauer et al. 2011
    Mass -> radius: M ~ R^2.06 (Earth units)
    Period -> semi-major axis: Kepler's third law (M_star * T^2)^(1/3)
"""

from systems.base import BaseSystem
from constants import radius_to_mass, period_to_a


class Kepler11(BaseSystem):
    name = "kepler11"
    star_mass = 1.042

    planets = [
        {"name": "b", "m": radius_to_mass(1.80), "a": period_to_a(10.30, star_mass)},
        {"name": "c", "m": radius_to_mass(2.87), "a": period_to_a(13.02, star_mass)},
        {"name": "d", "m": radius_to_mass(3.12), "a": period_to_a(22.68, star_mass)},
        {"name": "e", "m": radius_to_mass(4.19), "a": period_to_a(32.00, star_mass)},
        {"name": "f", "m": radius_to_mass(2.49), "a": period_to_a(46.69, star_mass)},
        {"name": "g", "m": radius_to_mass(3.33), "a": period_to_a(118.38, star_mass)},
    ]