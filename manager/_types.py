from dataclasses import dataclass
from enum import Enum

@dataclass
class OrbitalBody:
    mass: float
    a: float
    e: float
    inc: float
    Omega: float
    omega: float
    M: float

class JobCondition(Enum):
    CONDITION_CONTROL = 0
    CONDITION_PERTURBED = 1

@dataclass
class Star:
    mass: float
    radius: float


@dataclass
class IntegratorConfig:
    integrator: str
    duration: int
    timestep: int

@dataclass
class JobMetadata:
    job_id: int
    system_id: int
    condition: JobCondition
    schema_version: int = 1

@dataclass
class JobConfiguration:
    star: Star
    integrator: IntegratorConfig

@dataclass
class Job:
    metadata: JobMetadata
    configuration: JobConfiguration
    planets: list[OrbitalBody]
    perturber: OrbitalBody
    planet_count: int