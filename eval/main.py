import time
import argparse

import cv2
import numpy as np

from snn import SNN
from timer import FPS
from Stream import VideoStreamMono
from ImageProcessing import Algorithm
import Indicator
import motionFieldTemplate

ap = argparse.ArgumentParser()
ap.add_argument("-n", "--num-frames", type=int, default=1000, help="# of frames to loop over for FPS test")
ap.add_argument("-d", "--display", help="Whether or not frames should be displayed", action="store_true")
ap.add_argument("-p", "--picamera", help="whether or not the Raspberry Pi camera should be used", action="store_true")
args = vars(ap.parse_args())

frameHW = (64, 64)
vs = VideoStreamMono(usePiCamera=args["picamera"], resolution=frameHW).start()
time.sleep(2.0)
prvs = vs.readMono()

algo = Algorithm()
AllFlattenTemplates = motionFieldTemplate.createAllFlattenTemplate(64, 64)
snn = SNN()
led = Indicator.Indicator()

fps = FPS().start()
while not fps.isPassed(args["num_frames"]):
    curr = vs.readMono()
    FlattenFlow = algo.calculateOpticalFlow(prvs, curr).flatten()
    dottedFlow = motionFieldTemplate.dotWithTemplates(FlattenFlow, AllFlattenTemplates)

    if args["display"]:
        showFrame = cv2.resize(cv2.cvtColor(curr, cv2.COLOR_GRAY2BGR), (256, 256))
        cv2.imshow("Frame", curr)
        key = cv2.waitKey(1) & 0xFF

    prvs = curr
    snn.run(2000)
    neuron = snn.getMostActiveNeuron()
    led.turnOffAll()
    led.turnOn(neuron)
    print(neuron)
    fps.update()

led.turnOffAll()
fps.stop()
print("Elasped time: {:.3f}".format(fps.elapsed()))
print("Approx. FPS: {:.3f}".format(fps.fps()))

cv2.destroyAllWindows()
vs.stop()
