from constants import M_JUP
from systems.kepler11 import Kepler11
from spock import FeatureClassifier
from detector import Detector

model = FeatureClassifier()

sim = Kepler11(42, {"m": M_JUP, "a": 5.5})
simulation = sim.build()
#sim.summary()
#print(feature_model.predict_stable(simulation))

sim1 = Kepler11(seed=42).build()
print("No giant:", model.predict_stable(sim1))

# Test 2: with distant stable giant
sim2 = Kepler11(seed=42, outer_giant={"m": M_JUP, "a": 20.0}).build()
print("Distant giant:", model.predict_stable(sim2))

# Test 3: with close destabilizing giant
sim3 = Kepler11(seed=42, outer_giant={"m": 3*M_JUP, "a": 3.0}).build()
print("Close giant:", model.predict_stable(sim3))