from dataclasses import dataclass
from types import Literal

@dataclass
class UnstableDetection:
    event_type: Literal[
        "close_encounter_inner",
        "close_encounter_outer",
        "high_eccentricity",
        "ejection",
        "stellar_collision",
        "megno_divergence",
        "amd_unstable"
    ]
    time: float  # sim.t at detection
    body: str | None # hash of trigger body
    value: float | None # measured value that crossed threshold
    threshold: float | None # threshold that was crossed (hill radius?)