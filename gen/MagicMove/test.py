import unittest
import numpy as np
import defineTriangle

class TestTriangleMethods(unittest.TestCase):

    def test_shift(self):
        triangle = defineTriangle.Triangle()
        answer = np.array( [[10, 10], [20, 10], [10, 20]] ).astype(np.float32)
        shifted = triangle.shift(10, 10)
        self.assertTrue(np.array_equal(shifted, answer))

    def test_zoom(self):
        triangle = defineTriangle.Triangle()
        answer = np.array( [[10, 10], [20, 10], [10, 20]] ).astype(np.float32)
        scaled = triangle.zoom(2)
        self.assertTrue(np.array_equal(scaled, answer))



if __name__ == "__main__":
    unittest.main()
