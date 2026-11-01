from generator import GenerateSystem
from json_out import build_job
from _types import JobCondition, Star, IntegratorConfig, OrbitalBody
import json
import subprocess


star = Star(
    mass=1.989e30,
    radius=6.9634e8
)

integrator = IntegratorConfig(
    integrator="whfast",
    duration=315576000000,
    timestep=86400
)

sys: GenerateSystem = GenerateSystem(1)
result = sys.run()

job = build_job(
    job_id=1,
    system_id=1,
    condition=JobCondition.CONDITION_CONTROL.value,
    star=star,
    integrator=integrator,
    planets=sys.planets,
    perturber=sys.perturber
)

print(job)

worker = subprocess.Popen(
    [r"./cmake-build-debug/orbit_test.exe"],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=None,
    text=True,
    bufsize=1
)

try:
    # Send job
    worker.stdin.write(job + "\n")
    worker.stdin.flush()

    # Receive result
    result_json = worker.stdout.readlines()

    if not result_json:
        raise RuntimeError("C worker exited without returning a result")

    print("C stdout:", result_json)

finally:
    worker.stdin.close()
    worker.wait()