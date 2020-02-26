from threading import Thread

from picamera.array import PiRGBArray
from picamera import PiCamera
from gpiozero import LED
import cv2

import ImageProcessing

class PiVideoStreamMono:
    def __init__(self, resolution=(64, 64), framerate=32):
        self.camera = PiCamera()
        self.camera.resolution = resolution
        self.camera.framerate = framerate
        self.rawCapture = PiRGBArray(self.camera, size=resolution)
        self.stream = self.camera.capture_continuous(self.rawCapture,
            format="bgr", use_video_port=True)
        self.rawframe = None
        self.monoFrame = None
        self.stopped = False
        fwidth = resolution[0]
        fheight = resolution[1]
        self.preprocessor = ImageProcessing.VideoPreprocessor(fheight, fwidth)
        self.preprocessor.findSideToCrop()
        self.preprocessor.findCropPoints()
        self.sideLength = self.preprocessor.getSideLengthAfterCrop()

    def start(self):
        Thread(target=self.update, args=(), daemon=True).start()
        return self

    def update(self):
        for f in self.stream:
            self.rawframe = f.array
            self.rawCapture.truncate(0)
            self.rawframe = self.preprocessor.cropFrameIntoSquare(self.rawframe)
            self.frame = cv2.resize(self.rawframe, (64, 64), cv2.INTER_AREA)
            self.monoFrame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)

            if self.stopped:
                self.stream.close()
                self.rawCapture.close()
                self.camera.close()
                return

    def read(self):
        return True, self.rawframe, self.frame, self.monoFrame

    def stop(self):
        self.stopped = True


class PiIndicator():

    def __init__(self):
        upLight = LED(4)
        downLight = LED(17)
        leftLight = LED(27)
        rightLight = LED(22)
        zoominLight = LED(18)
        zoomoutLight = LED(23)
        rotatecwLight = LED(24)
        rotateccwLight = LED(25)
        avoidfront = LED(5)
        avoidrear = LED(6)
        avoidleft = LED(12)
        avoidright = LED(16)
        self.lookup = [ rotateccwLight, rotatecwLight, zoominLight, zoomoutLight, upLight, downLight, rightLight, leftLight,
                        avoidfront, avoidrear, avoidleft, avoidright ]

    def turnOn(self, index):
        self.lookup[index].on()

    def turnOnConfig(self, threshold, config):
        for index, activity in enumerate(config, start=0):
            if activity > threshold:
                self.lookup[index].on()

    def turnOffAll(self):
        for led in self.lookup:
            led.off()

    def turnOff(self, index):
        self.lookup[index].off()
