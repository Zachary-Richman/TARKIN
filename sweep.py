import constants
from runner import run, Run
from systems.SyntheticTestingSystem import SyntheticTestingSystem
from datetime import date, datetime
import constants as const
from simulator import config
from dataclasses import asdict
import csv
import sys

outer_giant_jup_multipliers = [0.3, 0.6, 1.0, 1.5, 2.0, 3.0]
outer_giant_a = [5, 7, 10, 13, 17, 22, 30]  # in AU
seeds = 50

# interval = 10yrs, total time = 10e6

metadata = f"""
# TARKIN Sweep Output
# Generated: {date.today()}
# REBOUND Version: latest <- fix
# T_MAX: {10e6}
# Check Interval: {10}
# DT: 0.001 years
# Integrator: {const.INTEGRATOR}
# giant_mass_multipliers: {outer_giant_jup_multipliers}
# giant_a's: {outer_giant_a}
# seeds: 0-{seeds}
"""

def sweep(mode = "full"):
    filename = f"tarkin_sweep_{mode}.txt"

    print(f"Starting sweep in {mode} mode")
    total_iterations = seeds * len(outer_giant_jup_multipliers) * len(outer_giant_a)
    iter_count = 0
    start_time = datetime.now()

    with open(filename, "w") as f:
        f.write(metadata)

    if mode == "full":
        for seed in range(seeds):
            for a in outer_giant_a:
                for m in outer_giant_jup_multipliers:
                    system = SyntheticTestingSystem(
                        seed=seed,
                        outer_giant={"m": const.M_JUP * m, "a": a}
                    )

                    with open(filename, "a") as file:
                        writer = csv.writer(file)
                        writer.writerow(asdict(run(system=system)).values())
                    iter_count += 1
                    print(f"[{iter_count}/{total_iterations}] {iter_count/total_iterations * 100:.2f}%  elapsed: {datetime.now() - start_time} eta: {((datetime.now() - start_time) / iter_count) * (total_iterations - iter_count)} last: {system.name}-{iter_count}-m{m}-a{a}")


if __name__ == "__main__":
    #if sys.argv[1] == "--test":
     #   print("Not set up")
    #else:
    sweep()