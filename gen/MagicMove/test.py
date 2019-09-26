import unittest
import numpy as np
import cv2
import DefineImagePattern
import GeometricTransform

class TestTrianglePatternMethods(unittest.TestCase):

    def setUp(self):
        self.triangle = DefineImagePattern.Triangle( [[0, 0], [10, 0], [10, 10], [0, 10]] )

    def test_getOriginal(self):
        answer = np.array( [[0, 0], [10, 0], [0, 10]] ).astype(np.float32)
        origin = self.triangle.getOriginal()
        self.assertTrue(np.array_equal(origin, answer))

    def test_getShifted(self):
        answer = np.array( [[10, 10], [20, 10], [10, 20]] ).astype(np.float32)
        shifted = self.triangle.getShifted(10, 10)
        self.assertTrue(np.array_equal(shifted, answer))

class TestSquarePatternMethods(unittest.TestCase):

    def setUp(self):
        self.square = DefineImagePattern.Square( [[0, 0], [10, 0], [10, 10], [0, 10]] )

    def test_getOriginal(self):
        answer = np.array( [[0, 0], [10, 0], [10, 10], [0, 10]] ).astype(np.float32)
        origin = self.square.getOriginal()
        self.assertTrue(np.array_equal(origin, answer))

    def test_getZoomed(self):
        answer = np.array( [[-10, -10], [20, -10], [20, 20], [-10, 20]] ).astype(np.float32)
        scaled = self.square.getZoomed(10, 10)
        self.assertTrue(np.array_equal(scaled, answer))

class TestAffineTransformationMethods(unittest.TestCase):

    def setUp(self):
        self.affine = GeometricTransform.AffineTransformation([[0, 0], [10, 0], [10, 10], [0, 10]])
        self.start = np.array( [[0, 0], [10, 0], [0, 10]] ).astype(np.float32)
        self.end = np.array( [[10, 10], [20, 10], [10, 20]] ).astype(np.float32)

    def test_getTransformationMatrix(self):
        matrix = self.affine.getTransformationMatrix(10, 10)
        answer = cv2.getAffineTransform(self.start, self.end)
        self.assertTrue(np.array_equal(matrix, answer))

    def test_camPanRight(self):
        pass

class TestPerspectiveTransformationMethods(unittest.TestCase):
    pass

if __name__ == "__main__":
    unittest.main()
