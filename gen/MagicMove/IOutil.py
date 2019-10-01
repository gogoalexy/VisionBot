import cv2
import sys
from Definitions import InfoCarrier

class ImageInput:

    def __init__(self, infoPacket):
        self.info = infoPacket
        imageName = self.info.getSourceImageName()
        self.image = cv2.imread(imageName)
    
    def getImage(self):
        return self.image

class VideoOutput:
    
    def __init__(self, infoPacket):
        self.info = infoPacket
        videoName = self.info.getDestinationVideoName()
        videoSize = (512, 512)
        videoFPS = 30.0
        fourcc = cv2.VideoWriter_fourcc(*'MJPG')
        self.video = cv2.VideoWriter(videoName, fourcc, videoFPS, videoSize)
    
    def writeImageIntoVideo(self, image):
        self.video.write(image)
    
    def terminateVideoStream(self):
        self.video.release()
