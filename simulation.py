from systems.kepler11 import Kepler11
from spock import FeatureClassifier

feature_model = FeatureClassifier()

sim = Kepler11(42, {"m": 31.57924e-05, "a": 5.5})
simulation = sim.build()
sim.summary()
print(feature_model.predict_stable(simulation))
