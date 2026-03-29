import numpy as np

CHECK_INTERVAL = 500 # years between checks
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

INNER_ORBIT_HORIZON = 1e9  # spock (tamayo et al. 2020) todo cite

MEGNO_CHAOTIC_THRESHOLD = 10.0
MEGNO_STABLE_THRESHOLD = 2.05
MEGNO_MIN_FRACTION = 0.05  # min frac of t_max before stable early stop\

AMD_UNSTABLE_FACTOR = 2
AMD_STABLE_FACTOR = 0.05


def radius_to_mass(radius):
    # uses the approximation m = r^2.06
    return (radius ** 2.06) * M_EARTH

def period_to_a(period_days, m_star):
    period = period_days * DAY
    return (m_star * period ** 2) ** (1 / 3)