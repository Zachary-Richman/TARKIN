import numpy as np


DAY = 1 / 365.25
M_EARTH = 3.003e-6 # solar masses
INTEGRATOR = "whfast"
DT = 0.001 # years
M_JUP = 9.548e-4 # solar masses
MAX_ECCENTRICITY = 0.9
E_DEFAULT: float = 0.0
INC_MAX = 0.05
TWO_PI = 2 * np.pi

MIN_PERIAPSIS = 0.01      # AU — stellar collision threshold
MAX_SEPARATION = 100.0  # AU, ejection threshold

# time intervals
T_SM = 1e4
T_MD = 1e6
T_LG = 1e9


def radius_to_mass(radius):
    # uses the approximation m = r^2.06
    return (radius ** 2.06) * M_EARTH

def period_to_a(period_days, m_star):
    period = period_days * DAY
    return (m_star * period ** 2) ** (1 / 3)