import cv2
import DefineImagePattern

class AffineTransformation:

    def __init__(self, imageBorder):
        self.triangle = DefineImagePattern.Triangle(imageBorder)

    def getTransformationMatrix(self, x, y):
        origin = self.triangle.getOriginal()
        transformed = self.triangle.getShifted(x, y)
        matrix = cv2.getAffineTransform(origin, transformed)
        return matrix

    def camShiftRight(self, start, end):
        pass


class PerspectiveTransformation:
    pass
