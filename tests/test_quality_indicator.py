import os
import unittest
import numpy as np

from kapylan.core.quality_indicator import HyperVolume
from pathlib import Path


class HyperVolumeTestCases(unittest.TestCase):
    def test_should_hypervolume_return_5_0(self):
        reference_point = [2, 2, 2]

        front = np.array([[1, 0, 1], [0, 1, 0]])

        hv = HyperVolume(reference_point)
        value = hv.compute(front)

        self.assertEqual(5.0, value)

    def test_should_hypervolume_return_the_correct_value_when_applied_to_the_ZDT1_reference_front(self):
        filepath = Path("resources/reference_front/", "ZDT1.pf")
        front = []

        with open(filepath) as file:
            for line in file:
                vector = [float(x) for x in line.split()]
                front.append(vector)

        reference_point = [1, 1]

        hv = HyperVolume(reference_point)
        value = hv.compute(np.array(front))

        self.assertAlmostEqual(0.666, value, delta=0.001)


if __name__ == "__main__":
    unittest.main()