import cv2
import sys

class ImageInput:

    def __init__(self):
        self.imageName = "NA"
        self.image = None
    
    def readImageName(self):
        try:
            self.imageName = sys.argv[1]
        except:
            self.imageName = "target.jpg"
    
    def readImage(self):
        self.image = cv2.imread(self.imageName)
    
    def getImage(self):
        return self.image

class VideoOutput:
    
    def __init__(self, videoName):
        self.videoName = videoName
    
    def writeImageIntoVideo(self):
        pass
    
    def terminateVideoStream(self):
        pass
