from core import constants
from core.constants import T_MD
from dataclasses import dataclass
from spock import FeatureClassifier
from assembly.detector import Detector, UnstableDetection
from core.simulator import config

@dataclass
class Run:
    run_id: str # {systemname}-{seed}-{giantmass}-{gianta}
    seed: int
    system_name: str
    giant_mass_mjup: float # measured in *M_JUP, 0.0 if no giant
    giant_a: float # measured in AU, 0.0 if no giant
    stable: bool
    instability_time: float
    detection_type: str  # "" if stable
    detection_body: str  # "" if stable
    detection_value: float  # -1 if stable
    detection_threshold: float  # -1 if stable
    spock_score_inner: float
    spock_score_full: float
    t_max: float
    check_interval: float


def run(system, t_max: float = T_MD, check_interval: float = 50.0) -> Run | None:
    """
    :param system:
    :param t_max:
    :param check_interval:
    :return:
    """
    outer_giant = system.outer_giant or {"m": 0.0, "a": 0.0}
    run_id = f"{system.name}-{system.seed}-{outer_giant['m']:.6f}-{int(outer_giant['a'])}"

    inner_system = system.__class__(seed=system.seed, outer_giant=None)
    sim_inner = config(inner_system)
    spock_inner = FeatureClassifier().predict_stable(sim_inner)

    sim_full = config(system.__class__(seed=system.seed, outer_giant=system.outer_giant))
    spock_full = FeatureClassifier().predict_stable(sim_full)


    # main integration
    sim = config(system)
    detector = Detector(sim)

    result = {
        "detection": None,
        "instability_time": -1
    }

    last_check = [0.0]  # mutable container so the closure can write to it

    def heartbeat(sim_pointer):
        t = sim_pointer.contents.t

        # throttle — only run the check every check_interval years
        if t - last_check[0] < check_interval:
            return
        last_check[0] = t

        #if int(t) % 10000 == 0:  # print every 10,000 years
        #    print(f"[{run_id}] heartbeat t={t:.0f}", flush=True)

        if result["detection"] is not None: return # detection found

        detection: None | UnstableDetection = detector.check()

        if detection is not None:
            result["detection"] = detection
            result["instability_time"] = sim_pointer.contents.t
            sim_pointer.contents.t = t_max + 1.0  # stop integration

    sim.heartbeat = heartbeat
    sim.heartbeat_dt = check_interval
    sim.integrate(t_max, exact_finish_time=0)

    return Run(  # TODO: just change result this is ugly ash
        run_id=run_id,
        seed=system.seed,
        system_name=system.name,
        giant_mass_mjup=outer_giant["m"] / constants.M_JUP,
        giant_a=outer_giant["a"],
        stable=result["detection"] is None,
        instability_time=result["instability_time"],
        detection_type=result["detection"].event_type if result["detection"] else "",
        detection_body=result["detection"].body if result["detection"] else "",
        detection_value=result["detection"].value if result["detection"] else -1.0,
        detection_threshold=result["detection"].threshold if result["detection"] else -1.0,
        spock_score_inner=float(spock_inner),
        spock_score_full=float(spock_full),
        t_max=t_max,
        check_interval=check_interval,
    )