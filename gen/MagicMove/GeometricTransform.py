import cv2
import numpy as np
import DefineImagePattern

class AffineTransformation:

    def __init__(self, image):
        self.image = np.array(image)
        self.imageHW = (self.image.shape[0], self.image.shape[1])
        self.imageBorder = [[0, 0], [self.imageHW[0]-1, 0], [self.imageHW[0]-1, self.imageHW[1]-1], [0, self.imageHW[1]-1]]

    def calculateTransformationMatrix(self, x, y):
        self.triangle = DefineImagePattern.Triangle(self.imageBorder)
        origin = self.triangle.getOriginal()
        transformed = self.triangle.getShifted(x, y)
        self.transformationMatrix = cv2.getAffineTransform(origin, transformed)

    def doTransformation(self):
        transformedImage = cv2.warpAffine(self.image, self.transformationMatrix, self.imageHW, borderValue=(255, 255, 255))
        return transformedImage


class PerspectiveTransformation:
    
    def __init__(self, image):
        self.image = np.array(image)
        self.imageHW = (self.image.shape[0], self.image.shape[1])
        self.imageBorder = [[0, 0], [self.imageHW[0]-1, 0], [self.imageHW[0]-1, self.imageHW[1]-1], [0, self.imageHW[1]-1]]
        
    def calculateTransformationMatrix(self, x, y):
        pass
    
    def doTransformation(self):
        pass
