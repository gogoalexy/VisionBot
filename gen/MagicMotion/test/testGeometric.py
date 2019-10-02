import sys
import unittest
import numpy as np
import cv2
sys.path.append('../src')
import DefineImagePattern
import GeometricTransform

class TestAffineTransformationMethods(unittest.TestCase):

    def setUp(self):
        self.image = cv2.imread("target.jpg")
        self.affine = GeometricTransform.AffineTransformation(self.image)
        start = np.array( [[0, 0], [self.image.shape[1]-1, 0], [0, self.image.shape[0]-1]] ).astype(np.float32)
        end = np.array( [[10, 10], [self.image.shape[1]+9, 10], [10, self.image.shape[0]+9]] ).astype(np.float32)
        self.transformationMatrix = cv2.getAffineTransform(start, end)

    def test_calculateTransformationMatrix(self):
        answer = self.transformationMatrix
        self.affine.calculateTransformationMatrix(10, 10)
        np.testing.assert_array_equal(self.affine.transformationMatrix, answer)

    def test_doTransformation(self):
        answer = cv2.warpAffine(self.image, self.transformationMatrix, (self.image.shape[1], self.image.shape[0]), borderValue=(255, 255, 255))
        self.affine.calculateTransformationMatrix(10, 10)
        out = self.affine.doTransformation()
        np.testing.assert_array_equal(out, answer)


class TestPerspectiveTransformationMethods(unittest.TestCase):

    def setUp(self):
        self.image = cv2.imread("target.jpg")
        self.affine = GeometricTransform.PerspectiveTransformation(self.image)
        start = np.array( [[0, 0], [self.image.shape[1]-1, 0], [self.image.shape[1]-1, self.image.shape[0]-1], [0, self.image.shape[0]-1]] ).astype(np.float32)
        end = np.array( [[-10, -10], [self.image.shape[1]+9, -10], [self.image.shape[1]+9, self.image.shape[0]+9], [-10, self.image.shape[0]+9]] ).astype(np.float32)
        self.transformationMatrix = cv2.getPerspectiveTransform(start, end)

    def test_calculateTransformationMatrix(self):
        answer = self.transformationMatrix
        self.affine.calculateTransformationMatrix(10, 10)
        np.testing.assert_array_equal(self.affine.transformationMatrix, answer)

    def test_doTransformation(self):
        answer = cv2.warpPerspective(self.image, self.transformationMatrix, (self.image.shape[1], self.image.shape[0]), borderValue=(255, 255, 255))
        self.affine.calculateTransformationMatrix(10, 10)
        out = self.affine.doTransformation()
        np.testing.assert_array_equal(out, answer)

class TestRotationTransformationMethods(unittest.TestCase):

    def setUp(self):
        self.image = cv2.imread("target.jpg")
        self.center = (self.image.shape[1]/2.0, self.image.shape[0]/2.0)
        self.affine = GeometricTransform.RotationTransformation(self.image)
        self.transformationMatrix = cv2.getRotationMatrix2D(self.center, 5, 1.0)

    def test_calculateTransformationMatrix(self):
        answer = self.transformationMatrix
        self.affine.calculateTransformationMatrix(5, 1.0)
        np.testing.assert_array_equal(self.affine.transformationMatrix, answer)

    def test_doTransformation(self):
        answer = cv2.warpAffine(self.image, self.transformationMatrix, (self.image.shape[1], self.image.shape[0]), borderValue=(255, 255, 255))
        self.affine.calculateTransformationMatrix(5, 1.0)
        out = self.affine.doTransformation()
        np.testing.assert_array_equal(out, answer)

if __name__ == "__main__":
    unittest.main()
