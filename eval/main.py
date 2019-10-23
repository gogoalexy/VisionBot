import time
import argparse

import cv2

from snn import SNN
from timer import FPS
from Stream import VideoStreamMono
from ImageProcessing import Algorithm
import Indicator
import motionFieldTemplate

ap = argparse.ArgumentParser()
framesToLoop = ap.add_mutually_exclusive_group()
framesToLoop.add_argument("-n", "--num-frames", type=int, default=1000, help="# of frames to loop over for FPS test")
framesToLoop.add_argument("-c", "--continuous", help="set number of frames to loop over to infinity", action="store_true")
ap.add_argument("-s", "--steps", type=int, default=500, help="# of steps to simulate for each frame")
ap.add_argument("-t", "--num-threads", type=int, default=1, help="# of threads to accelerate")
ap.add_argument("-d", "--display", help="Whether or not frames should be displayed", action="store_true")
ap.add_argument("-p", "--picamera", help="Whether or not the Raspberry Pi camera should be used", action="store_true")
ap.add_argument("-iz", "--izhikevich", help="Use Izhikevich neuron model instead of IQIF", action="store_true")
args = vars(ap.parse_args())

frameHW = (64, 64)
vs = VideoStreamMono(usePiCamera=args["picamera"], resolution=frameHW).start()
time.sleep(2.0)
prvs = vs.readMono()

algo = Algorithm()
AllFlattenTemplates = motionFieldTemplate.createAllFlattenTemplate(64, 64)
snn = SNN(args["izhikevich"], args["num_threads"])
led = Indicator.Indicator()

fps = FPS().start()
while True:
    curr = vs.readMono()
    FlattenFlow = algo.calculateOpticalFlow(prvs, curr).flatten()
    dottedFlow = motionFieldTemplate.dotWithTemplates(FlattenFlow, AllFlattenTemplates)
    normalizedDottedFlow = [ int(dotted/500) for dotted in dottedFlow ]

    if args["display"]:
        showFrame = cv2.resize(cv2.cvtColor(curr, cv2.COLOR_GRAY2BGR), (256, 256))
        cv2.imshow("Frame", curr)
        key = cv2.waitKey(1) & 0xFF

    prvs = curr
    snn.stimulateInOrder(normalizedDottedFlow)
    snn.run(args["steps"])
    activity = snn.getAllActivityInOrder()
    print(activity)
    led.turnOffAll()
    led.turnOnConfig(3, activity)
    fps.update()
    if not args["continuous"] and fps.isPassed(args["num_frames"]):
        break

led.turnOffAll()
fps.stop()
print("Elasped time: {:.3f} s".format(fps.elapsed()))
print("Approx. average FPS: {:.3f}".format(fps.fps()))

cv2.destroyAllWindows()
vs.stop()
