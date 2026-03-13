import rebound
from core.constants import INTEGRATOR, DT

def config(system) -> rebound.Simulation:
    sim = system.build()
    sim.integrator = INTEGRATOR
    sim.dt = DT
    return sim