# Tarkin 
Trajectory Analysis and Resonance Klassifier for Inner N-body systems (TARKIN)

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11+-blue?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/Python-3.11+-blue?style=plastic&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/Python-3.11+-blue?style=social&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/Python-3.11+-blue?style="for-the-badge"&logo=python&logoColor=white"/>
</p>

----
Thousands of multi-planet systems discovered by NASA's Kepler Space Telescope contain small planets packed tightly 
together in very close orbits around their host star. Whether these systems remain stable over billions of years, or whether gravitational 
interactions will eventually cause collisions or ejections, is a longstanding open question in orbital dynamics.


In 2020, researchers at Princeton published SPOCK (Stability of Planetary Orbital Configurations Klassifier), 
a machine learning model that predicts the long-term stability of compact planetary systems at orders of magnitude faster than running full N-body simulations. 
SPOCK represented a major advance in computational astrophysics, but it was trained exclusively on systems with no outer companion planets.
Many real Kepler systems, however, include a distant giant planet, whose slow and persistent gravitational influence on the inner system is entirely unaccounted for in SPOCK's predictions. 
## Research Question
> Does the presence of an outer giant companion systematically degrade SPOCK's predictive accuracy on compact inner systems; and if so, at what giant mass and orbital separation does this effect become significant?

## An Empirical Motivation
Before building anything, I ran SPOCK on the first three planets (`b`, `c`, `d`) of the Kepler 11 system under three conditions:

| Condition              | SPOCK Score |
|------------------------|-------------|
| No outer giant         | 0.919       |
| 1 M_Jup giant at 20 AU | 0.791       |
| 3 M_Jup giant at 3 AU  | 0.791       |

```python
from core.constants import M_JUP
from systems.kepler11 import Kepler11
from spock import FeatureClassifier

model = FeatureClassifier()

sim1 = Kepler11(seed=42).build()
print("No giant:", model.predict_stable(sim1))  # 0.9192146

# Test 2: with distant stable giant
sim2 = Kepler11(seed=42, outer_giant={"m": M_JUP, "a": 20.0}).build()
print("Distant giant:", model.predict_stable(sim2))  # 0.79106146

# Test 3: with close destabilizing giant
sim3 = Kepler11(seed=42, outer_giant={"m": 3 * M_JUP, "a": 3.0}).build()
print("Close giant:", model.predict_stable(sim3))  # 0.79106146
```

SPOCK's predicted stability probability is statistically invariant to the outer giant's presence; 
even when a 3 Jupiter-mass companion orbits at 3 AU, well within the range expected to produce measurable secular forcing on the inner system. 


## Methodology
**Phase 1 - Determining if SPOCK Fails (and if so, characterize it)**

Using [REBOUND](https://rebound.hanno-rein.de/), a high-precision N-body integration package, we simulate compact inner planetary systems both with and without an outer companion.
Then, we run SPOCK's classifier on each system and compare its predicted stability against the truth from full integration. 

**Phase 2 - Generate a new training dataset**

An automated pipeline runs across a grid of outer giant parameters

| Parameter               | Range                     | Values |
|-------------------------|---------------------------|--------|
| Giant Mass              | 0.3-3.0 * Mass of Jupiter | 6      |
| Semi-major axis         | 5-30 AU                   | 7      |
| Seeds per Configuration | n/a                       | 25     |
| Total Runs              | n/a                       | 1050   |
**Phase 3 - Train an extended classifier**

We train a standalone XGBoost Classifier on the now generated dataset. Unlike SPOCK, TARKIN treats the outer
giants properties (`mass`, `semi-major axis`, `period`, `hill stability margin`) as additional inputs alongside the inner-system features.

## Design Decisions
**WHFast > IAS515**. 
The WHFast sympletic integrator conserves a modified Hamiltonian exactly over long timescale and runs 10-100x faster that REBOUND's default integrator. 

**Log uniform planet masses**.
Synthetic planet masses are drawn log-uniformly from 1–20 Earth masses, matching the observed Kepler compact system population (Fabrycky et al. 2012) and avoiding overrepresentation of high-mass planets.


## References
 
- Tamayo et al. 2020: [SPOCK: Predicting Planetary Stability](https://arxiv.org/abs/2007.06521)
- Pu & Wu 2015: [Spacing of Kepler Planets](https://iopscience.iop.org/article/10.1088/0004-637X/807/1/44)
- Fabrycky et al. 2012: [Architecture of Kepler's Multi-Transiting Systems](https://arxiv.org/abs/1202.6328)
- Rein & Tamayo 2015: [REBOUND: WHFast](https://arxiv.org/abs/1506.01084)
- Livesey & Becker 2024: [Giant Planet Companions and Inner System Stability](https://arxiv.org/abs/2412.18661)

This project is still very much under development and does not claim to make any scientific claims. As a student, I intend to learn and develop with time, the programming and scientific journey will be documented in this repository.
