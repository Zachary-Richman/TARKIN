import constants
from constants import T_MD, T_LG, T_SM
from dataclasses import dataclass, asdict
from spock import FeatureClassifier
from detector import Detector, UnstableDetection
from simulator import config

@dataclass
class Run:
    run_id: str # {systemname}-{seed}-{giantmass}-{gianta}
    seed: int
    system_name: str
    giant_mass_mjup: float # measured in *M_JUP, 0.0 if no giant
    giant_mass_a: float # measured in AU, 0.0 if no giant
    stable: bool
    instability_time: float
    detection: UnstableDetection | None
    spock_score: any
    t_max: float
    check_interval: float


def run(system, t_max: float = T_MD, check_interval: float = 10.0) -> Run | None:
    """

    :param system:
    :param t_max:
    :param check_interval:
    :return:
    """
    sim = config(system)

    # spock without the outer giant
    inner_system = system.__class__(seed=system.seed, outer_giant=None)
    sim_inner = config(inner_system)
    spock_prediction_score = FeatureClassifier().predict_stable(sim_inner)

    detector = Detector(sim)

    outer_giant = system.outer_giant
    if not outer_giant:
        outer_giant = {
            "m": 0.0,
            "a": 0.0
        }

    t = 0
    instability_time = -1
    detection = None
    run_id = f"{system.name}-{system.seed}-{outer_giant["m"]}-{outer_giant["a"]}"

    while t < t_max:
        t += check_interval
        checker: UnstableDetection | None = detector.check(t)
        if checker is not None:
            instability_time = t
            detection = checker
            #print(detection)
            break
        #print(f"[SIMULATION]: {run_id} ({t}/{t_max})")

    return Run(
        run_id=run_id,
        seed=system.seed,
        system_name=system.name,
        giant_mass_mjup=outer_giant["m"] / constants.M_JUP,
        giant_mass_a=outer_giant["a"],
        stable=(True if instability_time < 0 else False),
        instability_time=instability_time,
        detection=detection,
        spock_score=spock_prediction_score,
        t_max=t_max,
        check_interval=check_interval,
    )