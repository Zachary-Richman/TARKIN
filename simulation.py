from systems.kepler11 import Kepler11
from spock import FeatureClassifier

feature_model = FeatureClassifier()

sim = Kepler11(42, {m: 3.57924e-05, a: 0.55})
sim.build()
sim.summary()
print(feature_model.predict_stable(sim.sim))