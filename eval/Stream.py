from threading import Thread

import cv2
import platform

import ImageProcessing

class VideoStreamMono:

    def __init__(self, src=0, usePiCamera=False, resolution=(640, 480), framerate=32):
        if usePiCamera:
            from PiOnly import PiVideoStreamMono
            self.stream = PiVideoStreamMono(resolution=resolution, framerate=framerate)
        else:
            if platform.system() == "Linux":
                src= 0 + cv2.CAP_V4L2
            self.stream = WebcamVideoStreamCroppedMono(src=src)

    def start(self):
        return self.stream.start()

    def update(self):
        self.stream.update()

    def read(self):
        return self.stream.read()

    def readMono(self):
        return self.stream.readMono()

    def stop(self):
        self.stream.stop()


class WebcamVideoStreamCroppedMono:

    def __init__(self, src = 0):
        self.stream = cv2.VideoCapture(src)
        (self.grabbed, rawframe) = self.stream.read()
        self.frame = None
        self.monoFrame = None
        self.stopped = False
        fwidth = int( self.stream.get(cv2.CAP_PROP_FRAME_WIDTH) )
        fheight = int( self.stream.get(cv2.CAP_PROP_FRAME_HEIGHT) )
        self.preprocessor = ImageProcessing.VideoPreprocessor(fheight, fwidth)
        self.preprocessor.findSideToCrop()
        self.preprocessor.findCropPoints()

    def start(self):
        Thread(target=self.update, args=(), daemon=True).start()
        return self

    def update(self):
        while True:
            if self.stopped:
                return

            (self.grabbed, rawframe) = self.stream.read()
            rawframe = self.preprocessor.cropFrameIntoSquare(rawframe)
            self.frame = cv2.resize(rawframe, (64, 64), cv2.INTER_AREA)
            self.monoFrame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)

    def read(self):
        return self.frame

    def readMono(self):
        return self.monoFrame

    def stop(self):
        self.stopped = True

