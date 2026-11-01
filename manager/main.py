from generator import GenerateSystem
from json_out import build_job
from _types import JobCondition, Star, IntegratorConfig, OrbitalBody

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