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
        self.image = cv2.imread("target.jpg")
        self.resultImage = cv2.imread("target_shift10-10.jpg")
        self.affine = GeometricTransform.AffineTransformation(self.image)
        start = np.array( [[0, 0], [self.image.shape[0]-1, 0], [0, self.image.shape[1]-1]] ).astype(np.float32)
        end = np.array( [[10, 10], [self.image.shape[0]+9, 10], [10, self.image.shape[1]+9]] ).astype(np.float32)
        self.transformationMatrix = cv2.getAffineTransform(start, end)

    def test_calculateTransformationMatrix(self):
        answer = self.transformationMatrix
        self.affine.calculateTransformationMatrix(10, 10)
        self.assertTrue(np.array_equal(self.affine.transformationMatrix, answer))

    def test_doTransformation(self):
        answer = self.resultImage
        self.affine.calculateTransformationMatrix(10, 10)
        out = self.affine.doTransformation()
        cv2.imwrite("test.jpg", out)
        difference = cv2.subtract(out, answer)
        b, g, r = cv2.split(difference)
        print(cv2.countNonZero(b))
        print(cv2.countNonZero(g))
        print(cv2.countNonZero(r))
        self.assertTrue(np.array_equal(out, answer))


class TestPerspectiveTransformationMethods(unittest.TestCase):

    def setUp(self):
        self.image = cv2.imread("target.jpg")
        self.affine = GeometricTransform.PerspectiveTransformation(self.image)
        self.start = np.array( [[0, 0], [10, 0], [10, 10], [0, 10]] ).astype(np.float32)
        self.end = np.array( [[-10, -10], [20, -10], [20, 20], [-10, 20]] ).astype(np.float32)
        self.transformationMatrix = cv2.getPerspectiveTransform(self.start, self.end)


if __name__ == "__main__":
    unittest.main()
