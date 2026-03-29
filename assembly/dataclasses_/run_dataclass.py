"""
assembly/dataclasses_/run_dataclass.py
=========================
Per-run dataclass for the TARKIN parameter sweep.

Each instance corresponds to a single row in the output file.
All fields are flat primitive types (no nested dicts, c types, or non-serializable objects),
so that dataclasses.asdict() produces a directly CSV-writable dict without required post-processing.

Field Groupings:
* Run identification: run_id, seed, system_name, giant_mass_mjup, giant_a, p_inner, check_interval
* Stability outcomes: stable, instability_time, detection_type, detection_body, detection_value, detection_threshold
* Spock outcomes: spock_score_inner, spock_score_full
* Dynamic indicators: megno_final, stable_early, t_max
* AMD indicators: amd_inner, amd_full, amd_critical
* Data quality indicators: rebound_version, spock_version, had_convergence_warning

References:
[1] Tamayo et al. 2020
    https://arxiv.org/abs/2007.06521
[2] Laskar & Petit 2017
    https://www.aanda.org/articles/aa/pdf/2017/09/aa30022-16.pdf
"""
from dataclasses import dataclass, fields

@dataclass
class FeatureExtraction:
    m: str

@dataclass
class Run(FeatureExtraction):
    run_id: str  # {system name}-{seed}-{giant mass}-{giant a}
    seed: int
    system_name: str
    giant_mass_mjup: float
    giant_a: float
    p_inner: float  # innermost particle orbital period (years)
    check_interval: float

    stable: bool
    instability_time: float
    detection_type: str
    detection_body: str
    detection_value: float
    detection_threshold: float

    spock_score_inner: float  # no giant
    spock_score_full: float  # with giant

    t_max: float  # p_inner * 1e9 [1]
    megno_final: float  # value at termination
    stable_early: bool  # evals true if terminated early bc/ MEGNO confidence

    amd_inner: float  # amd of inner system (no giant)
    amd_full: float  # amd of full system (including giant)
    amd_critical: float  # critical AMD threshold [2]

    had_convergence_warning: bool  # true if WHFast timestep warning fired
    spock_version: str
    rebound_version: str

    @staticmethod
    def to_headers() -> list[str]:
        """Return: ordered list of field names for CSV headers."""
        return [f.name for f in fields(Run)]