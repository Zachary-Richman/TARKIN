"""
assembly/runner.py
==================
Single simulation run for the sweep

Run (class) completes a simulation from initial conditions
It will return a full run object to be later classified
No state is shared between calls, making parallelization simple

This is the only model that should call sim.integrate()


"""
import rebound
from assembly.handlers.amd import AMD


class Runner(AMD):
    def __init__(self, system):
        self.system = system

