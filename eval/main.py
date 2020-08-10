import time
import argparse

import cv2
import numpy as np

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
ap.add_argument("-dp", "--display-potential", help="Whether or not neural potentials should be displayed", action="store_true")
ap.add_argument("-do", "--display-obstacle", help="Whether or not obstacles should be displayed", action="store_true")
ap.add_argument("-dd", "--display-dot", help="Whether or not dotted results should be displayed", action="store_true")
ap.add_argument("-df", "--display-flow", help="Whether or not flow frames should be displayed", action="store_true")
ap.add_argument("-demo", "--demo-nov", help="Whether to get into graphical demo mode", action="store_true")
ap.add_argument("-i", "--input", type=str, help="Input video file instead of live stream.")
ap.add_argument("-o", "--output", type=str, help="Output processed video file for obstacle detection.")
ap.add_argument("-p", "--picamera", help="Whether or not the Raspberry Pi camera should be used", action="store_true")
ap.add_argument("--port", type=int, default=0, help="Receive video stream from a UDP port")
ap.add_argument("-iz", "--izhikevich", help="Use Izhikevich neuron model instead of IQIF", action="store_true")
args = vars(ap.parse_args())

# Order: ROTATECW, ZOOMIN, DOWN, RIGHT, ROTATECCW, ZOOMOUT, UP, LEFT, outer[UP, Rear, Left, Right], middle[UP, Rear, Left, Right], inner[UP, Rear, Left, Right], center, modeInh(not shown), obsInh(not shown)
label =  "CW  FWD DWN RT CCW  BWD  UP  LFT oUP oLFT oRT oDWN mUP mLFT mRT mDWN iUP iLFT iRT iDWN C"
frameHW = (320, 240)
frameRate = 32

if args["input"]:
    vs = VideoStreamMono(src=args["input"], usePiCamera=False, resolution=frameHW, framerate=frameRate).start()
elif args["port"] != 0:
    vs = VideoStreamMono(usePiCamera=False, rtsp_port=args["port"], resolution=frameHW, framerate=frameRate).start()
else:
    vs = VideoStreamMono(usePiCamera=args["picamera"], resolution=frameHW, framerate=frameRate).start()

if args["output"]:
    fourcc = cv2.VideoWriter_fourcc(*"MJPG")
    saver = cv2.VideoWriter(args["output"] + '.avi', fourcc, 30, (512, 512))
else:
    saver = None

time.sleep(2.0)

algo = Algorithm()
[ret, raw, _, prvs] = vs.read()
#prvs = algo.contrastEnhance(prvs)

AllFlattenTemplates = motionFieldTemplate.readAllFlattenTemplate()
snn = SNN(args["izhikevich"], args["num_threads"])
#led = Indicator.Indicator()

if args["display_flow"]:
    guiFlow = Graphics.Flow()

if args["display_dot"]:
    guiDot = Graphics.Dot()

if args["display_neuron"]:
    guiNeuron = Graphics.Neuron()

if args["display_potential"]:
    potentials = [0]
    guiPotential = Graphics.Potential(snn.getNumNeurons())

if args["display_obstacle"]:
    guiObstacle = Graphics.Obstacle(threshold = 5, saver=saver)

if args["demo_nov"]:
    guiDemo = Graphics.Demo()
    guiDemo.mountWindowAt(0, 0)
    showFrame = cv2.resize(cv2.cvtColor(prvs, cv2.COLOR_GRAY2BGR), (256, 256))
    #cv2.imshow("Preview", showFrame)
    #cv2.moveWindow("Preview", 1055, 35)

prvsActivity = [0] * 21
fps = FPS().start()
localfps = FPS().start()
realtimeFPS = 0
counter = 0
prvsDottedFlow = [0] * 8
prvsAvoidCurrents = [0] * 13

[ret, raw, _, curr] = vs.read()
key = cv2.waitKey(1)
while ret and key & 0xFF != ord('q'):
    start = time.time()

    #curr = algo.contrastEnhance(curr)
    [ret, raw, _, curr] = vs.read()

    if (not args["input"]) and np.array_equal(curr, prvs):
        print("Identical frame skipped.({:d})".format(counter))
        continue

    # calculate dense optical flow
    FlattenFlow = algo.calculateOpticalFlow(prvs, curr).flatten()
    meanFlattenFlow = motionFieldTemplate.meanOpticalFlow(FlattenFlow).flatten()

    # inner products of measured and template flows for motion compensation
    dottedFlow = motionFieldTemplate.dotWithTemplatesOpt(meanFlattenFlow, AllFlattenTemplates)
    normalizedDottedFlow = [ dotted / 10.0 for dotted in dottedFlow ]
    movingAvgNormalizedDottedFlow = list( map(lambda x, y: x*0.2 + y*0.8, normalizedDottedFlow, prvsDottedFlow) )

    # same as above, but are local for obstacle avoidance
    avoidCurrents = motionFieldTemplate.obstacleAvoidanceCurrent(meanFlattenFlow, AllFlattenTemplates)
    weightedAvoidCurrents = [ avoid * 3.0 for avoid in avoidCurrents ]
    weightedAvoidCurrents = np.abs(avoidCurrents)
    movingAvgWeightedAvoidCurrents = list( map(lambda x, y: x*0.2 + y*0.8, weightedAvoidCurrents, prvsAvoidCurrents) )

    # generate neuron input currents
    neuronCurrents = list( map(int, movingAvgNormalizedDottedFlow + movingAvgWeightedAvoidCurrents) )

    # IQIF simulation
    snn.stimulateInOrder(neuronCurrents)
    #snn.run(args["steps"])
    for index in range(args["steps"]):
        snn.run(1)
        if args["display_potential"]:
            potentials = potentials + snn.getAllPotential()
    #activity = list( map(lambda x, y: x*0.25 + y*0.75, snn.getFirstNActivityInOrder(21), prvsActivity) )
    activity = snn.getFirstNActivityInOrder(21)


    if args["display_flow"]:
        guiFlow.display(raw, meanFlattenFlow, realtimeFPS)

    if args["display_dot"]:
        guiDot.display(raw, label, normalizedDottedFlow, realtimeFPS)

    if args["display_neuron"]:
        guiNeuron.display(raw, label, realtimeFPS, activity)

    if args["display_potential"]:
        potentials = potentials[-500 * snn.getNumNeurons():]
        guiPotential.display(potentials, snn.getNumNeurons())

    if args["display_obstacle"]:
        guiObstacle.display(raw, activity, realtimeFPS)

    if args["demo_nov"] and counter % 3 == 0:
        guiDemo.displayConfig((1, 1), activity)
        #showFrame = cv2.resize(cv2.cvtColor(curr, cv2.COLOR_GRAY2BGR), (256, 256))
        #cv2.putText(showFrame, "FPS={:.1f}".format(realtimeFPS), (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (5, 255, 5))
        #cv2.imshow("Preview", showFrame)

    prvs = curr
    prvsDottedFlow = movingAvgNormalizedDottedFlow
    prvsAvoidCurrents = movingAvgWeightedAvoidCurrents
    prvsActivity = activity
    #led.turnOffAll()
    #led.turnOnConfig(3, activity)
    fps.update()
    localfps.update()
    counter += 1
    if localfps.isPassed(30):
        localfps.stop()
        realtimeFPS = localfps.fps()
        localfps.reset()
        localfps.start()
    if not args["continuous"] and fps.isPassed(args["num_frames"]):
        break
    end = time.time()
    if args["input"]:
        remaining = 1/frameRate - (end-start)
        remaining = remaining * (remaining > 0)
        #time.sleep(remaining)

    key = cv2.waitKey(1)

#led.turnOffAll()
fps.stop()
print("Elasped time: {:.3f} s".format(fps.elapsed()))
print("Approx. average FPS: {:.3f}".format(fps.fps()))

cv2.destroyAllWindows()
if saver != None:
    saver.release()
vs.stop()
