import rebound
from core.constants import INTEGRATOR

def config(system) -> rebound.Simulation:
    sim = system.build()
    sim.integrator = INTEGRATOR

    innermost = sim.particles[1].orbit(primary="star")
    DT =  innermost.P # twenty steps per innermost orbit per iteration (years)
    sim.dt = DT

    sim.ri_whfast.safe_mode = 0 # skip Jacobi coord sync
    sim.ri_whfast.corrector = 11

    return sim
