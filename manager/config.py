version = "0.0.1"  # for later flagging of iterations

# houses all the constants
m_jup = 1.899e+27 # kg
m_sun = 1.9891e+30  # kg
m_earth = 5.9722e24  # kg
au = 1.495978707e11  # m
r_sun = 695700000  # m
# ----- Utilized in the Program -----
n_values = range(2, 9)  # n = 2...8
total_systems = 105000
min_planets = 2
max_planets = 8
sys_per_n_value = total_systems // max_planets  # divide and floor

m_planet_min = 1.0 * m_earth
m_planet_max = 20.0 * m_earth
innermost_a = 0.3 * au  # a_1 -> semimajor axis of the first planet from the sun


integration_time = 10e5
integrator = "whfast"

max_eccentricity: float = 0.9
eccentricity_default: float = 0.0
inclination_max: float = 0.05

m_perturber: int = m_jup * 6.0 # kg
a_additional_perturber: int = au * 3  # m?


