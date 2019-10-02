import sys
import unittest
sys.path.append("../")
import Definitions

class testInfoCarrier(unittest.TestCase):

    def test_accessSourceImageName(self):
        legalName = "test.jpg"
        illegalName = 888
        carrier = Definitions.InfoCarrier()
        carrier.setSourceImageName(legalName)
        self.assertEqual(carrier.getSourceImageName(), legalName)
        self.assertRaises(AssertionError, carrier.setSourceImageName, illegalName)

    def test_accessDestinationVideoName(self):
        legalName = "test.avi"
        illegalName = 999
        carrier = Definitions.InfoCarrier()
        carrier.setDestinationVideoName(legalName)
        self.assertEqual(carrier.getDestinationVideoName(), legalName)
        self.assertRaises(AssertionError, carrier.setDestinationVideoName, illegalName)

    def test_accessMovePattern(self):
        legalPattern = Definitions.MovePattern.NA
        illegalPattern = 1.1
        carrier = Definitions.InfoCarrier()
        carrier.setMovePattern(legalPattern)
        self.assertEqual(carrier.getMovePattern(), legalPattern)
        self.assertRaises(AssertionError, carrier.setMovePattern, illegalPattern)

    def test_accessMoveDirection(self):
        legalDirection = Definitions.Rotate.NA
        illegalDirection = 7
        carrier = Definitions.InfoCarrier()
        carrier.setMoveDirection(legalDirection)
        self.assertEqual(carrier.getMoveDirection(), legalDirection)
        self.assertRaises(AssertionError, carrier.setMoveDirection, illegalDirection)

    def test_accesssStartPoint(self):
        legalPoint = (6, 9)
        illegalPoint = 10
        carrier = Definitions.InfoCarrier()
        carrier.setStartPoint(legalPoint)
        self.assertEqual(carrier.getStartPoint(), legalPoint)
        self.assertRaises(AssertionError, carrier.setStartPoint, illegalPoint)

    def test_accessDuration(self):
        legalDuration = 18
        illegalDuration = 18.0
        carrier = Definitions.InfoCarrier()
        carrier.setDuration(legalDuration)
        self.assertEqual(carrier.getDuration(), legalDuration)
        self.assertRaises(AssertionError, carrier.setDuration, illegalDuration)

    def test_accessSpeed(self):
        legalSpeed = 0.0
        illegalSpeed = 16
        carrier = Definitions.InfoCarrier()
        carrier.setSpeed(legalSpeed)
        self.assertEqual(carrier.getSpeed(), legalSpeed)
        self.assertRaises(AssertionError, carrier.setSpeed, illegalSpeed)

if __name__ == "__main__":
    unittest.main()
