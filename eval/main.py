import time
import argparse

import cv2

from snn import SNN
from timer import FPS
from Stream import VideoStreamMono
from ImageProcessing import Algorithm
import Indicator
import Graphics
import motionFieldTemplate

ap = argparse.ArgumentParser()
framesToLoop = ap.add_mutually_exclusive_group()
framesToLoop.add_argument("-n", "--num-frames", type=int, default=1000, help="# of frames to loop over for FPS test")
framesToLoop.add_argument("-c", "--continuous", help="Set number of frames to loop over to infinity", action="store_true")
ap.add_argument("-s", "--steps", type=int, default=50, help="# of steps to simulate for each frame")
ap.add_argument("-t", "--num-threads", type=int, default=1, help="# of threads to accelerate")
ap.add_argument("-dn", "--display-neuron", help="Whether or not neural activities should be displayed", action="store_true")
ap.add_argument("-dd", "--display-dot", help="Whether or not dotted results should be displayed", action="store_true")
ap.add_argument("-df", "--display-flow", help="Whether or not flow frames should be displayed", action="store_true")
ap.add_argument("-demo", "--demo-nov", help="Whether to get into graphical demo mode", action="store_true")
ap.add_argument("-i", "--input", type=str, help="Input video file instead of live stream.")
ap.add_argument("-p", "--picamera", help="Whether or not the Raspberry Pi camera should be used", action="store_true")
ap.add_argument("-iz", "--izhikevich", help="Use Izhikevich neuron model instead of IQIF", action="store_true")
args = vars(ap.parse_args())
# Order: ROTATECW, ROTATECCW, ZOOMIN, ZOOMOUT, DOWN, UP, RIGHT, LEFT
label = "CW CCW  IN  OUT  DWN UP  RT  LFT wFRT wRR wLT wRT"
frameHW = (64, 64)
frameRate = 32
if args["input"]:
    vs = VideoStreamMono(src=args["input"], usePiCamera=False, resolution=frameHW, framerate=frameRate).start()
else:
    vs = VideoStreamMono(usePiCamera=args["picamera"], resolution=frameHW, framerate=frameRate).start()

time.sleep(2.0)
prvs = vs.readMono()

algo = Algorithm()
AllFlattenTemplates = motionFieldTemplate.readAllFlattenTemplate()
snn = SNN(args["izhikevich"], args["num_threads"])
led = Indicator.Indicator()
gui = Graphics.Graphics()

fps = FPS().start()
localfps = FPS().start()
realtimeFPS = 0
while True:
    curr = vs.readMono()
    FlattenFlow = algo.calculateOpticalFlow(prvs, curr).flatten()
    dottedFlow = motionFieldTemplate.dotWithTemplatesOpt(FlattenFlow, AllFlattenTemplates)
    normalizedDottedFlow = [ int(dotted/500) for dotted in dottedFlow ]
    snn.stimulateInOrder(normalizedDottedFlow)
    snn.run(args["steps"])
    activity = snn.getAllActivityInOrder()

    if args["display_flow"]:
        showFrame = curr.copy()
        interval = 8
        for y in range(4, 64, 8):
            for x in range(4, 64, 8):
                cv2.line(showFrame, (x, y), (x+int(FlattenFlow[y*128+2*x]), y+int(FlattenFlow[y*128+2*x+1])), color=(255, 255, 255))
        showFrame = cv2.resize(cv2.cvtColor(showFrame, cv2.COLOR_GRAY2BGR), (512, 512))
        cv2.putText(showFrame, "FPS={:.1f}".format(realtimeFPS), (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (5, 255, 5))
        cv2.imshow("Flow", showFrame)
        cv2.waitKey(1)

    if args["display_dot"]:
        showFrame = cv2.resize(cv2.cvtColor(curr, cv2.COLOR_GRAY2BGR), (512, 512))
        interval = 40
        cv2.putText(showFrame, label, (15, 350), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255))
        cv2.putText(showFrame, "FPS={:.1f}".format(realtimeFPS), (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (5, 255, 5))
        for loc, val in enumerate(normalizedDottedFlow):
            cv2.line(showFrame, (25+loc*interval, 300), (25+loc*interval, 300-val*30), color=(255, 55, 255), thickness=20)
        cv2.imshow("Dotted", showFrame)
        cv2.waitKey(1)

    if args["display_neuron"]:
        showFrame = cv2.resize(cv2.cvtColor(curr, cv2.COLOR_GRAY2BGR), (512, 512))
        interval = 40
        cv2.putText(showFrame, label, (15, 480), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255))
        cv2.putText(showFrame, "FPS={:.1f}".format(realtimeFPS), (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (5, 255, 5))
        for loc, val in enumerate(activity):
            cv2.line(showFrame, (25+loc*interval, 450), (25+loc*interval, 450-val*20), color=(255, 255, 55), thickness=15)
        cv2.imshow("Neuron", showFrame)
        cv2.waitKey(1)

    if args["demo_nov"]:
        gui.displayConfig((2, 2), activity)

    prvs = curr
    led.turnOffAll()
    led.turnOnConfig(2, activity)
    fps.update()
    localfps.update()
    if localfps.isPassed(30):
        localfps.stop()
        realtimeFPS = localfps.fps()
        localfps.reset()
        localfps.start()
    if not args["continuous"] and fps.isPassed(args["num_frames"]):
        break

led.turnOffAll()
fps.stop()
print("Elasped time: {:.3f} s".format(fps.elapsed()))
print("Approx. average FPS: {:.3f}".format(fps.fps()))

cv2.destroyAllWindows()
vs.stop()
