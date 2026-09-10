# Tarkin 
Trajectory Analysis and Resonance Klassifier for Inner N-body systems (TARKIN)

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11+-blue?style=plastic&logo=python&logoColor=white"/>
</p>

----
Thousands of multi-planet systems discovered by NASA's Kepler Space Telescope contain small planets packed tightly 
together in very close orbits around their host star. Whether these systems remain stable over billions of years, or whether gravitational 
interactions will eventually cause collisions or ejections, is a longstanding open question in orbital dynamics.


## Research Question
> How does the number of planets in a [compact planetary system] affect the fraction of systems that remain stable over a fixed time interval following the introduction of an additional outer gravitational perturber at a larger semi-major axis and constant mass `[m = 6 * M_jup]`?

## Methodology
**Phase 1 - Generating Data (and if so, characterize it)**

Using [REBOUND](https://rebound.hanno-rein.de/), a high-precision N-body integration package, we simulate compact inner planetary systems both with and without an outer companion.
Within this phase, we will cleanse the data, (see `/Assembly`) in order to avoid initially unstable conditions

**Phase 2 - Training dataset**

An automated pipeline runs across a grid of outer giant parameters

| Parameter               | Values/Range              | 
|-------------------------|---------------------------|
| Giant Mass              | 6 * Mass of Jupiter       |
| Semi-major axis         | 30 AU                     |
| Seeds per Configuration | 4000                      |
| Total Runs              | 24000                     |

**Phase 3 - Train an extended classifier**

We (may) train a standalone XGBoost Classifier on the now generated dataset. 

## Design Decisions
**WHFast > IAS515**. 
The WHFast sympletic integrator conserves a modified Hamiltonian exactly over long timescale and runs 10-100x faster that REBOUND's default integrator. 

## References
 
- Tamayo et al. 2020: [SPOCK: Predicting Planetary Stability](https://arxiv.org/abs/2007.06521)
- Pu & Wu 2015: [Spacing of Kepler Planets](https://iopscience.iop.org/article/10.1088/0004-637X/807/1/44)
- Fabrycky et al. 2012: [Architecture of Kepler's Multi-Transiting Systems](https://arxiv.org/abs/1202.6328)
- Rein & Tamayo 2015: [REBOUND: WHFast](https://arxiv.org/abs/1506.01084)
- Livesey & Becker 2024: [Giant Planet Companions and Inner System Stability](https://arxiv.org/abs/2412.18661)

This project is still very much under development and does not claim to make any scientific claims. As a student, I intend to learn and develop with time, the programming and scientific journey will be documented in this repository.
