import sys
import unittest
from unittest import mock
sys.path.append("../")
import UserInterface
from Definitions import MovePattern, Zoom, Pan, Rotate

class testUserInterface(unittest.TestCase):

    def test_collectInputImageName(self):
        testName = "test.jpg"
        interface = UserInterface.UserInterface()
        with mock.patch("builtins.input", return_value=testName):
            interface.collectInputImageName()
        self.assertEqual(interface.infoPacket.getSourceImageName(), testName)

    def test_collectOutputVideoName(self):
        testName = "test.avi"
        interface = UserInterface.UserInterface()
        with mock.patch("builtins.input", return_value=testName):
            interface.collectOutputVideoName()
        self.assertEqual(interface.infoPacket.getDestinationVideoName(), testName)

    def test_collectMovePattern(self):
        legalOption = '1'
        legalAnswer = MovePattern.ZOOM
        illegalOption = '8'
        interface = UserInterface.UserInterface()
        with mock.patch("builtins.input", return_value=legalOption):
            interface.collectMovePattern()
        self.assertEqual(interface.infoPacket.getMovePattern(), legalAnswer)
        with mock.patch("builtins.input", return_value=illegalOption):
            self.assertRaises(SystemExit, interface.collectMovePattern)

    def test_collectMoveDirection(self):
        legalOption = '1'
        legalAnswer = Zoom.IN
        illegalOption = '8'
        interface = UserInterface.UserInterface()
        interface.pattern = MovePattern.ZOOM
        with mock.patch("builtins.input", return_value=legalOption):
            interface.collectMoveDirection()
        self.assertEqual(interface.infoPacket.getMoveDirection(), legalAnswer)
        with mock.patch("builtins.input", return_value=illegalOption):
            self.assertRaises(SystemExit, interface.collectMoveDirection)

    def test_collectStartPoint(self):
        legalPoint = '6 4'
        legalAnswer = (6, 4)
        illegalPoint = '64'
        interface = UserInterface.UserInterface()
        with mock.patch("builtins.input", return_value=legalPoint):
            interface.collectStartPoint()
        self.assertEqual(interface.infoPacket.getStartPoint(), legalAnswer)
        with mock.patch("builtins.input", return_value=illegalPoint):
            self.assertRaises(SystemExit, interface.collectStartPoint)

    def test_collectDuration(self):
        legalDuration = '11'
        legalAnswer = 11
        illegalDuration = 'uwu'
        interface = UserInterface.UserInterface()
        with mock.patch("builtins.input", return_value=legalDuration):
            interface.collectDuration()
        self.assertEqual(interface.infoPacket.getDuration(), legalAnswer)
        with mock.patch("builtins.input", return_value=illegalDuration):
            self.assertRaises(SystemExit, interface.collectDuration)

    def test_collectSpeed(self):
        legalSpeed = '4'
        legalAnswer = 4.0
        illegalSpeed = 'u45'
        interface = UserInterface.UserInterface()
        with mock.patch("builtins.input", return_value=legalSpeed):
            interface.collectSpeed()
        self.assertEqual(interface.infoPacket.getSpeed(), legalAnswer)
        with mock.patch("builtins.input", return_value=illegalSpeed):
            self.assertRaises(SystemExit, interface.collectSpeed)

    @unittest.skip("All cases have been tested above.")
    def test_gatherEssentialParametersFromUser(self):
        pass

if __name__ == "__main__":
    unittest.main()
