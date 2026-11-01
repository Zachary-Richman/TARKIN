import json
from dataclasses import asdict
from _types import (
    JobCondition, Star, IntegratorConfig, OrbitalBody,
    Job, JobMetadata, JobConfiguration
)


def build_job(
    job_id: int,
    system_id: int,
    condition: JobCondition,
    star: Star,
    integrator: IntegratorConfig,
    planets: list[OrbitalBody | dict],
    perturber: OrbitalBody | dict
) -> Job:

    if not planets:
        raise ValueError("A job must contain at least one inner planet.")

    if not isinstance(condition, int):
        raise TypeError("condition must be a JobCondition.")

    def to_orbital_body(body):
        if isinstance(body, OrbitalBody):
            return body

        return OrbitalBody(
            mass=float(body["mass"]),
            a=float(body["a"]),
            e=float(body["e"]),
            inc=float(body["inc"]),
            Omega=float(body["Omega"]),
            omega=float(body["omega"]),
            M=float(body["M"])
        )

    return json.dumps(asdict(Job(
        metadata=JobMetadata(
            job_id=job_id,
            system_id=system_id,
            condition=condition
        ),
        configuration=JobConfiguration(
            star=star,
            integrator=integrator
        ),
        planets=[to_orbital_body(planet) for planet in planets],
        perturber=to_orbital_body(perturber),
        planet_count=len(planets)
    )))