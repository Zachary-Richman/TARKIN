import csv
import os
import ray
from core import constants as const
from dataclasses import asdict, fields
from datetime import datetime, date
from assembly.runner import run, Run
import rebound
from systems.SyntheticTestingSystem import SyntheticTestingSystem

OUTER_GIANT_JUP_MULTIPLIER = [0.3, 0.6, 1.0, 1.5, 2.0, 3.0]
OUTER_GIANT_A = [5, 7, 10, 13, 17, 22, 30]  # in AU
SEED = 100
T_MAX = 1000000
CHECK_INTERVAL = 1
HEADERS = [f.name for f in fields(Run)]
FILENAME = "tarkin_sweep.csv"

metadata = f"""
# TARKIN Sweep Output
# Generated: {date.today()}
# REBOUND Version: {rebound.__version__}
# T_MAX: {T_MAX}
# Check Interval: {CHECK_INTERVAL}
# DT: 0.001 years
# Integrator: {const.INTEGRATOR}
# giant_mass_multipliers: {OUTER_GIANT_JUP_MULTIPLIER}
# giant_a's: {OUTER_GIANT_A}
# seeds: 0-{SEED - 1}
"""

@ray.remote
def run_simulation(seed: int, og_a: float | None, og_m: float | None) -> dict:
    if og_a is None or og_m is None:
        system = SyntheticTestingSystem(seed=seed, outer_giant=None)
    else:
        system = SyntheticTestingSystem(seed=seed, outer_giant={
            "m": const.M_JUP *  og_m,
            "a": og_a,
        })

    return asdict(run(system=system, t_max=T_MAX, check_interval=CHECK_INTERVAL))

def _combo_to_run_id(seed: int, a: float | None, m: float | None) -> str:  # converts the tuple to a run identifier
    if a is None:
        return f"synthetic-{seed}-0.000000-0"
    return f"synthetic-{seed}-{const.M_JUP * m:.6f}-{int(a)}"

# def _run_id_to_combo(combo: str) -> tuple: <- TODO

def sweep():
    all_combos = []  # long term we can track which ones have been done in the csv file for pause/resume work

    for seed in range(SEED):
        all_combos.append((seed, None, None))  # control
        for a in OUTER_GIANT_A:
            for m in OUTER_GIANT_JUP_MULTIPLIER:
                all_combos.append((seed, a, m))

    completed_ids = []  # FUTURE: this can read the csv, add completed tuple groups (see TODO above function) and pick up when failures happen

    pending = [
        c for c in all_combos
        if _combo_to_run_id(*c) not in completed_ids
    ]

    if not pending:
        print("Sweep already completed...")
        return

    # write headers if not exists
    if not os.path.exists(FILENAME):
        with open(FILENAME, "w") as f:
            f.write(metadata)
            csv.writer(f).writerow(HEADERS)

    # Ray uses all cores by default, num_cpus=x can limit
    ray.init(ignore_reinit_error=True, num_cpus=4)
    print("[SWEEP] Ray Initialized")

    futures = [run_simulation.remote(seed, a, m) for seed, a, m, in pending]

    completed = 0
    failed = 0
    start = datetime.now()

    with open(FILENAME, "a") as f:
        writer = csv.writer(f)

        while futures: # while tasks are still left
            done, futures = ray.wait(futures, num_returns=1, timeout=600)

            if not done:  # timeout hit w/ no resp
                print(f"[SWEEP] Warning: No task complete in 10 minutes. {len(futures)} futures remaining.")
                continue

            try:
                result = ray.get(done[0])
                writer.writerow(result.values())
                f.flush()
                completed += 1

                elapsed = datetime.now() - start
                rate = completed / elapsed.total_seconds()
                remaining = len(futures)
                eta = (remaining / rate) if rate > 0 else 0  # to prevent div by zero error

                print(
                    f"[{completed}/{len(futures)}] {(completed / len(futures)) * 100:.1f}% "
                    f"rate: {rate:.1f}/s "
                    f"remaining: {eta / 60:.1f}min "
                    f"id: {result['run_id']}"
                )

            except Exception as e:
                failed += 1
                print(f"[FAILED] {e}")

    ray.shutdown()
    elapsed = datetime.now() - start
    print("Sweep complete.")
    print(f"Completed: {completed} | Failed: {failed} | Total time: {elapsed}")


if __name__ == "__main__":
    sweep()