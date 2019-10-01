import sys
import cv2
import unittest
from unittest import mock
from numpy import testing
sys.path.append("../")
import IOutil
from Definitions import InfoCarrier

class TestImageInput(unittest.TestCase):
    
    def test_getImage(self):
        testName = "lenna_full.jpg"
        answer = cv2.imread(testName)
        info = InfoCarrier()
        info.getSourceImageName = mock.MagicMock(return_value=testName)
        self.inputModule = IOutil.ImageInput(info)
        testing.assert_array_equal(self.inputModule.getImage(), answer)
    
class TestVideoOutput(unittest.TestCase):

    def test_init(self):
        info = InfoCarrier()
        info.getDestinationVideoName = mock.MagicMock(return_value="test.avi")
        self.outputModule = IOutil.VideoOutput(info)
        status = self.outputModule.video.isOpened()
        self.assertTrue(status)

if __name__ == "__main__":
    unittest.main()

