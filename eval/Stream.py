from threading import Thread
import cv2
import ImageProcessing

class VideoStreamMono:

    def __init__(self, src=0, usePiCamera=False, resolution=(640, 480), framerate=32):
        if usePiCamera:
            from picamera.array import PiRGBArray
            from picamera import PiCamera
            self.stream = PiVideoStreamMono(resolution=resolution, framerate=framerate)
        else:
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

    def __init__(self, src=0):
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
            self.frame = cv2.resize(rawframe, (64, 64))
            self.monoFrame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)

    def read(self):
        return self.frame

    def readMono(self):
        return self.monoFrame

    def stop(self):
        self.stopped = True


class PiVideoStreamMono:
    def __init__(self, resolution=(64, 64), framerate=32):
        self.camera = PiCamera()
        self.camera.resolution = resolution
        self.camera.framerate = framerate
        self.rawCapture = PiRGBArray(self.camera, size=resolution)
        self.stream = self.camera.capture_continuous(self.rawCapture,
            format="bgr", use_video_port=True)
        self.frame = None
        self.monoFrame = None
        self.stopped = False

    def start(self):
        Thread(target=self.update, args=(), daemon=True).start()
        return self

    def update(self):
        for f in self.stream:
            self.frame = f.array
            self.rawCapture.truncate(0)
            self.monoFrame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)

            if self.stopped:
                self.stream.close()
                self.rawCapture.close()
                self.camera.close()
                return

    def read(self):
        return self.frame

    def readMono(self):
        return self.monoFrame

    def stop(self):
        self.stopped = True
