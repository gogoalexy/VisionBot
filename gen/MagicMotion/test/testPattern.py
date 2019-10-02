import sys
import unittest
import numpy as np
sys.path.append('../')
import DefineImagePattern

class TestTrianglePatternMethods(unittest.TestCase):

    def setUp(self):
        self.triangle = DefineImagePattern.Triangle( [[0, 0], [10, 0], [10, 10], [0, 10]] )

    def test_getOriginal(self):
        answer = np.array( [[0, 0], [10, 0], [0, 10]] ).astype(np.float32)
        origin = self.triangle.getOriginal()
        np.testing.assert_array_equal(origin, answer)

    def test_getShifted(self):
        answer = np.array( [[10, 10], [20, 10], [10, 20]] ).astype(np.float32)
        shifted = self.triangle.getShifted(10, 10)
        np.testing.assert_array_equal(shifted, answer)

class TestSquarePatternMethods(unittest.TestCase):

    def setUp(self):
        self.square = DefineImagePattern.Square( [[0, 0], [10, 0], [10, 10], [0, 10]] )

    def test_getOriginal(self):
        answer = np.array( [[0, 0], [10, 0], [10, 10], [0, 10]] ).astype(np.float32)
        origin = self.square.getOriginal()
        np.testing.assert_array_equal(origin, answer)

    def test_getZoomed(self):
        answer = np.array( [[-10, -10], [20, -10], [20, 20], [-10, 20]] ).astype(np.float32)
        scaled = self.square.getZoomed(10, 10)
        np.testing.assert_array_equal(scaled, answer)
        

if __name__ == "__main__":
    unittest.main()

