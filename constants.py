DAY = 1 / 365.25
M_EARTH = 3.003e-6 # solar masses
INTEGRATOR = "whfast"
DT = 0.001 # years
M_JUP = 9.548e-4 # solar masses
MAX_ECCENTRICITY = 0.9

def radius_to_mass(radius):
    # uses the approximation m = r^2.06
    return (radius ** 2.06) * M_EARTH

def period_to_a(period_days, m_star):
    period = period_days * DAY
    return (m_star * period ** 2) ** (1 / 3)