# temporary

import numpy as np

from manager.generator import GenerateSystem


def test_all_multiplicities_generate():
    systems_per_n = 15_000

    for n in range(2, 9):
        system_id = (n - 2) * systems_per_n + 1
        system = GenerateSystem(system_id).run()

        assert len(system["planets"]) == n
        assert system["perturber"]["mass"] > 0


def test_reproducibility():
    first = GenerateSystem(1).run()
    second = GenerateSystem(1).run()

    assert first == second


def test_inner_planet_parameters_are_valid():
    system = GenerateSystem(1).run()

    planets = system["planets"]

    for planet in planets:
        assert planet["mass"] > 0
        assert planet["a"] > 0
        assert 0 <= planet["e"] < 1
        assert 0 <= planet["inc"] <= np.pi
        assert 0 <= planet["M"] < 2 * np.pi

    axes = [planet["a"] for planet in planets]
    assert axes == sorted(axes)