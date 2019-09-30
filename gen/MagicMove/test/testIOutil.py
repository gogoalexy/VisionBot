import sys
import cv2
import unittest
from unittest import mock
from numpy import testing
sys.path.append("../")
import IOutil

class TestImageInput(unittest.TestCase):

    def setUp(self):
        self.inputModule = IOutil.ImageInput()
    
    def test_readImageName(self):
        testName = ["anyway", "test.jpg"]
        with mock.patch("sys.argv", testName):
            self.inputModule.readImageName()
            self.assertEqual(self.inputModule.imageName, testName[1])
        self.inputModule.readImageName()
        self.assertEqual(self.inputModule.imageName, "target.jpg")

    def test_readImage(self):
        desiredImage = cv2.imread("lenna_full.jpg")
        self.inputModule.imageName = "lenna_full.jpg"
        self.inputModule.readImage()
        testing.assert_array_equal(self.inputModule.image, desiredImage)
    
    @unittest.skip("No need to test return statement.")
    def test_getImage(self):
        pass
    
class TestVideoOutput(unittest.TestCase):

    def setUp(self):
        self.outputModule = IOutil.VideoOutput()
        

if __name__ == "__main__":
    unittest.main()

