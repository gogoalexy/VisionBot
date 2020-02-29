import time
import argparse

import cv2
import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui

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
ap.add_argument("-p", "--picamera", help="Whether or not the Raspberry Pi camera should be used", action="store_true")
ap.add_argument("-iz", "--izhikevich", help="Use Izhikevich neuron model instead of IQIF", action="store_true")
args = vars(ap.parse_args())
# Order: ROTATECCW, ZOOMIN, UP, RIGHT, ROTATECW, ZOOMOUT, DOWN, LEFT, outer[UP, Rear, Left, Right], middle[UP, Rear, Left, Right], inner[UP, Rear, Left, Right], center, modeInh(not shown), obsInh(not shown)
label =  "CW  FWD DWN RT CCW  BWD  UP  LFT oUP oLFT oRT oDWN mUP mLFT mRT mDWN iUP iLFT iRT iDWN C"
frameHW = (640, 480)
frameRate = 32
if args["input"]:
    vs = VideoStreamMono(src=args["input"], usePiCamera=False, resolution=frameHW, framerate=frameRate).start()
else:
    vs = VideoStreamMono(usePiCamera=args["picamera"], resolution=frameHW, framerate=frameRate).start()

time.sleep(2.0)

algo = Algorithm()
[ret, raw, _, prvs] = vs.read()
prvs = algo.contrastEnhance(prvs)

AllFlattenTemplates = motionFieldTemplate.readAllFlattenTemplate()
snn = SNN(args["izhikevich"], args["num_threads"])
#led = Indicator.Indicator()

if args["display_flow"]:
    guiFlow = Graphics.Flow()

if args["demo_nov"]:
    guiDemo = Graphics.Demo()
    guiDemo.mountWindowAt(0, 0)
    showFrame = cv2.resize(cv2.cvtColor(prvs, cv2.COLOR_GRAY2BGR), (256, 256))
    #cv2.imshow("Preview", showFrame)
    #cv2.moveWindow("Preview", 1055, 35)

if args["display_potential"]:
    potentials = [0]
    potentialY = np.full(2000, 255)
    win = pg.GraphicsWindow()
    win.setWindowTitle('Potentials')
    curvePotentials = [0] * snn.getNumNeurons()
    for index in range(snn.getNumNeurons()):
        if index % 4 == 0:
            win.nextRow()
        plotPotentials = win.addPlot()
        plotPotentials.setYRange(-10, 260, padding=0)
        curvePotentials[index] = plotPotentials.plot(potentialY)

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

    curr = algo.contrastEnhance(curr)
    
    # calculate dense optical flow 
    # note the different parameters between old and new Farneback
    FlattenFlow = algo.calculateOpticalFlow(prvs, curr).flatten()
    meanFlattenFlow = motionFieldTemplate.meanOpticalFlow(FlattenFlow).flatten()
    
    # inner products of measured and template flows for motion compensation
    dottedFlow = motionFieldTemplate.dotWithTemplatesOpt(meanFlattenFlow, AllFlattenTemplates)
    normalizedDottedFlow = [ dotted / 10.0 for dotted in dottedFlow ]
    movingAvgNormalizedDottedFlow = list( map(lambda x, y: x*0.25 + y*0.75, normalizedDottedFlow, prvsDottedFlow) )
    
    # same as above, but are local for obstacle avoidance
    avoidCurrents = motionFieldTemplate.obstacleAvoidanceCurrent(meanFlattenFlow, AllFlattenTemplates)
    #weightedAvoidCurrents = [ avoid * 0.23 for avoid in avoidCurrents ]
    weightedAvoidCurrents = avoidCurrents
    movingAvgWeightedAvoidCurrents = list( map(lambda x, y: x*0.5 + y*0.5, weightedAvoidCurrents, prvsAvoidCurrents) )
    
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
        guiFlow.displayFlow(raw, meanFlattenFlow, realtimeFPS)

    if args["display_dot"]:
        showFrame = raw.copy()
        showFrame = cv2.resize(showFrame, (512, 512))
        interval = 40
        cv2.putText(showFrame, label[0:33], (15, 350), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255))
        cv2.putText(showFrame, "FPS={:.1f}".format(realtimeFPS), (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (5, 255, 5))
        for loc, val in enumerate(normalizedDottedFlow):
            cv2.line(showFrame, (25+loc*interval, 300), (25+loc*interval, 300-int(val*2)), color=(255, 55, 255), thickness=20)
        cv2.imshow("Dotted", showFrame)

    if args["display_neuron"]:
        showFrame = raw.copy()
        showFrame = cv2.resize(showFrame, (512, 512))
        interval = 40
        cv2.putText(showFrame, label[0:32], (15, 480), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255))
        cv2.putText(showFrame, "FPS={:.1f}".format(realtimeFPS), (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (5, 255, 5))
        for loc, val in enumerate(activity):
            cv2.line(showFrame, (25+(loc%8)*interval, 512-(62*(1+loc//8))), (25+(loc%8)*interval, 512-(62*(1+loc//8))-int(val)*20), color=(255, 255, 55), thickness=15)
        cv2.imshow("Neuron", showFrame)

    if args["display_potential"]:
        potentials = potentials[-2000 * snn.getNumNeurons():]
        npPotentials = np.zeros(2000 * snn.getNumNeurons())
        npPotentials[-len(potentials):] = np.array(potentials)
        npPotentials = npPotentials.reshape(2000, snn.getNumNeurons())
        for index in range(snn.getNumNeurons()):
            curvePotentials[index].setData(npPotentials[:, index])

    if args["display_obstacle"]:
        showFrame = raw.copy()
        showFrame = cv2.resize(showFrame, (512, 512))
        
        cv2.line(showFrame, (0, 0), (192, 192), (0, 0, 0), 2)
        cv2.line(showFrame, (320, 320), (512, 512), (0, 0, 0), 2)
        cv2.line(showFrame, (0, 512), (192, 320), (0, 0, 0), 2)
        cv2.line(showFrame, (512, 0), (320, 192), (0, 0, 0), 2)
        cv2.rectangle(showFrame, (64, 64), (448, 448), (0, 0, 0), 2)
        cv2.rectangle(showFrame, (128, 128), (384, 384), (0, 0, 0), 2)
        cv2.rectangle(showFrame, (192, 192), (320, 320), (0, 0, 0), 2)
        
        pts = np.array([[2, 0], [511, 0], [446, 62], [64, 62]], np.int)
        pts = pts.reshape((-1, 1, 2))
        if activity[8] > 1:
            cv2.polylines(showFrame, [pts], True, (0, 255, 0), 12)
        pts = np.array([[0, 2], [0, 511], [62, 446], [62, 64]], np.int)
        pts = pts.reshape((-1, 1, 2))
        if activity[9] > 1:
            cv2.polylines(showFrame, [pts], True, (0, 255, 0), 12)
        pts = np.array([[511, 2], [511, 510], [448, 446], [448, 64]], np.int)
        pts = pts.reshape((-1, 1, 2))
        if activity[10] > 1:
            cv2.polylines(showFrame, [pts], True, (0, 255, 0), 12)
        pts = np.array([[2, 511], [510, 511], [446, 448], [64, 448]], np.int)
        pts = pts.reshape((-1, 1, 2))
        if activity[11] > 1:
            cv2.polylines(showFrame, [pts], True, (0, 255, 0), 12)

        pts = np.array([[64, 64], [446, 64], [384, 126], [128, 126]], np.int)
        pts = pts.reshape((-1, 1, 2))
        if activity[12] > 1:
            cv2.polylines(showFrame, [pts], True, (0, 255, 0), 12)
        pts = np.array([[64, 64], [64, 446], [126, 384], [126, 128]], np.int)
        pts = pts.reshape((-1, 1, 2))
        if activity[13] > 1:
            cv2.polylines(showFrame, [pts], True, (0, 255, 0), 12)
        pts = np.array([[446, 64], [446, 446], [384, 382], [384, 128]], np.int)
        pts = pts.reshape((-1, 1, 2))
        if activity[14] > 1:
            cv2.polylines(showFrame, [pts], True, (0, 255, 0), 12)
        pts = np.array([[64, 446], [446, 446], [382, 384], [128, 384]], np.int)
        pts = pts.reshape((-1, 1, 2))
        if activity[15] > 1:
            cv2.polylines(showFrame, [pts], True, (0, 255, 0), 12)

        pts = np.array([[128, 128], [382, 128], [318, 190], [192, 190]], np.int)
        pts = pts.reshape((-1, 1, 2))
        if activity[16] > 1:
            cv2.polylines(showFrame, [pts], True, (0, 255, 0), 12)
        pts = np.array([[128, 128], [128, 382], [190, 318], [190, 192]], np.int)
        pts = pts.reshape((-1, 1, 2))
        if activity[17] > 1:
            cv2.polylines(showFrame, [pts], True, (0, 255, 0), 12)
        pts = np.array([[382, 128], [382, 382], [320, 318], [320, 192]], np.int)
        pts = pts.reshape((-1, 1, 2))
        if activity[18] > 1:
            cv2.polylines(showFrame, [pts], True, (0, 255, 0), 12)
        pts = np.array([[128, 382], [382, 382], [318, 320], [192, 320]], np.int)
        pts = pts.reshape((-1, 1, 2))
        if activity[19] > 1:
            cv2.polylines(showFrame, [pts], True, (0, 255, 0), 12)

        if activity[20] > 1:
            cv2.rectangle(showFrame, (192, 192), (318, 318), (0, 255, 0), 12)

        cv2.putText(showFrame, "FPS={:.1f}".format(realtimeFPS), (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (5, 255, 5))
        cv2.imshow("Obstacles", showFrame)

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
    [ret, raw, _, curr] = vs.read()

#led.turnOffAll()
fps.stop()
print("Elasped time: {:.3f} s".format(fps.elapsed()))
print("Approx. average FPS: {:.3f}".format(fps.fps()))

cv2.destroyAllWindows()
vs.stop()
