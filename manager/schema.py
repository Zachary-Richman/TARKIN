import math
from typing import Any


req_orbital_fields = {
    "name",
    "mass",
    "a",
    "e",
    "inc",
    "Omega",
    "omega",
    "M",
}


def validate_body(body: dict[str, Any]) -> None:
    missing = req_orbital_fields - body.keys()

    if missing:
        raise ValueError(
            f"Missing orbital fields for "
            f"{body.get('name', '<unnamed>')}: {sorted(missing)}"
        )

    for field in ("mass", "a", "e", "inc", "Omega", "omega", "M"):
        value = body[field]

        if not isinstance(value, (int, float)) or isinstance(value, bool):
            raise ValueError(f"{field} must be numeric.")

        if not math.isfinite(value):
            raise ValueError(f"{field} must be finite.")

    if body["mass"] <= 0:
        raise ValueError("Mass must be positive.")

    if body["a"] <= 0:
        raise ValueError("Semimajor axis must be positive.")

    # Bound elliptical orbit; e = 1 is parabolic, not elliptical.
    if not 0 <= body["e"] < 1:
        raise ValueError("Eccentricity must satisfy 0 <= e < 1.")

    if not 0 <= body["inc"] <= math.pi:
        raise ValueError("Inclination must be in [0, pi].")

    for field in ("Omega", "omega", "M"):
        if not 0 <= body[field] < 2 * math.pi:
            raise ValueError(f"{field} must be in [0, 2*pi).")


def validate_job(job: dict[str, Any]) -> None:
    required = {
        "schema_version",
        "job_id",
        "system_id",
        "condition",
        "seed",
        "units",
        "star",
        "planets",
        "perturber",
        "integration",
    }

    missing = required - job.keys()

    if missing:
        raise ValueError(
            f"Missing required job fields: {sorted(missing)}"
        )

    if job["schema_version"] != 1:
        raise ValueError("Unsupported schema version.")

    if job["condition"] not in {"control", "perturbed"}:
        raise ValueError("Condition must be 'control' or 'perturbed'.")

    if not isinstance(job["planets"], list) or not job["planets"]:
        raise ValueError("Planets must be a non-empty list.")

    if not isinstance(job["star"], dict):
        raise ValueError("Star must be a dictionary.")

    if not isinstance(job["star"].get("mass"), (int, float)):
        raise ValueError("Star mass must be numeric.")

    if not math.isfinite(job["star"]["mass"]) or job["star"]["mass"] <= 0:
        raise ValueError("Star mass must be finite and positive.")

    for planet in job["planets"]:
        validate_body(planet)

    if job["condition"] == "control":
        if job["perturber"] is not None:
            raise ValueError("Control jobs must not contain a perturber.")
    else:
        if not isinstance(job["perturber"], dict):
            raise ValueError("Perturbed jobs require a perturber dictionary.")

        validate_body(job["perturber"])

    if not isinstance(job["integration"], dict):
        raise ValueError("Integration settings must be a dictionary.")

    duration = job["integration"].get("duration")

    if (
        not isinstance(duration, (int, float))
        or isinstance(duration, bool)
        or not math.isfinite(duration)
        or duration <= 0
    ):
        raise ValueError("Integration duration must be finite and positive.")
