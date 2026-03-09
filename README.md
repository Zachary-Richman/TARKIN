# Tarkin 
Trajectory Analysis and Resonance Klassifier for Inner N-body systems (TARKIN)

> Extending SPOCK, a Princeton developed machine learning stability classifier, to compact planetary systems with outer giant companions

## Overview
Thousands of multi-planet systems discovered by NASA's Kepler Space Telescope contain small planets packed tightly 
together in very close orbits around their host star. Whether these systems remain stable over billions of years, or whether gravitational 
interactions will eventually cause collisions or ejections, is a longstanding open question in orbital dynamics. In 2020, researchers at Princeton published SPOCK (Stability of Planetary Orbital Configurations Klassifier), 
a machine learning model that predicts the long-term stability of compact planetary systems at orders of magnitude faster than running full N-body simulations. 
SPOCK represented a major advance in computational astrophysics, but it was trained exclusively on systems with no outer companion planets.
Many real Kepler systems, however, include a distant giant planet, whose slow and persistent gravitational influence on the inner system is entirely unaccounted for in SPOCK's predictions. 
**Like Grand Moff Tarkin commanding from a distance, the outer giant exerts outsized destructive reach on everything closer to the star.**

## Research Question
> Does the presence of an outer giant companion degrade SPOCK's predictive accuracy on compact inner systems? And, can a retrained model incorporating outer giant parameters recover that accuracy?

## Methodology
**Phase 1 - Determining if SPOCK Fails (and if so, characterize it)**
Using Rebound, a high-precision N-body integration package, we simulate compact inner planetary systems both with and without an outer companion.
Then, we run SPOCK's classifier on each system and compare its predicted stability against the ground truth from full integration. 
If SPOCK's predictions fail under new conditions (as hypothesized), then we proceed to phase 2 and 3.

**Phase 2 - Generate a new training dataset**
We build an automated pipeline that systematically sweeps the outer giant parameter space with varying mass from 0.3 to 3 Jupiter masses and semi-major axis from 5 to 30 AU.
We run thousands of REBOUND simulations and recording instability timescales. 
Each run produces one row in the training dataset.

**Phase 3 - Train an extended classifier**
We train an XGBoost classifier on the new dataset, incorporating SPOCK's original feature set plus `outer giant mass`, `semi-major axis`, and `mass ratio` as additional input features. 
We compare the extended model's accuracy against vanilla SPOCK on a held-out test set of systems with outer giant companions.

TODO: source and attributions to this readme