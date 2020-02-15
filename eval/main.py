import time
import argparse

import cv2
import matplotlib.pyplot as plt
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
ap.add_argument("-p", "--picamera", help="Whether or not the Raspberry Pi camera should be used", action="store_true")
ap.add_argument("-iz", "--izhikevich", help="Use Izhikevich neuron model instead of IQIF", action="store_true")
args = vars(ap.parse_args())
# Order: ROTATECCW, ZOOMIN, UP, RIGHT, ROTATECW, ZOOMOUT, DOWN, LEFT, outer[UP, Rear, Left, Right], middle[UP, Rear, Left, Right], inner[UP, Rear, Left, Right], center, modeInh(not shown), obsInh(not shown)
label =  "CCW IN   UP  RT  CW  OUT DWN  LFT oUP oLFT oRT oDWN mUP mLFT mRT mDWN iUP iLFT iRT iDWN C"
frameHW = (64, 64)
frameRate = 30
if args["input"]:
    vs = VideoStreamMono(src=args["input"], usePiCamera=False, resolution=frameHW, framerate=frameRate).start()
else:
    vs = VideoStreamMono(usePiCamera=args["picamera"], resolution=frameHW, framerate=frameRate).start()

time.sleep(2.0)

algo = Algorithm()
prvs = vs.readMono()
prvs = algo.contrastEnhance(prvs)

AllFlattenTemplates = motionFieldTemplate.readAllFlattenTemplate()
snn = SNN(args["izhikevich"], args["num_threads"])
#led = Indicator.Indicator()
gui = Graphics.Graphics()

if args["demo_nov"]:
    gui.mountWindowAt(0, 0)
    showFrame = cv2.resize(cv2.cvtColor(prvs, cv2.COLOR_GRAY2BGR), (256, 256))
    cv2.imshow("Preview", showFrame)
    cv2.moveWindow("Preview", 1055, 35)

if args["display_potential"]:
    ax = [0] * snn.getNumNeurons()
    axbackground = [0] * snn.getNumNeurons()
    plt.ion()
    potentials = []
    potentialX = np.arange(250)
    potentialY = np.full(250, 255)
    figPotential = plt.figure()
    line = [0] * snn.getNumNeurons()
    for index in range(snn.getNumNeurons()):
        ax[index] = figPotential.add_subplot(snn.getNumNeurons() // 4 + 1*bool(snn.getNumNeurons()%4), 4, index + 1)
        ax[index].set_ylim([-10, 256])
        line[index], = ax[index].plot(potentialX, potentialY, 'r-')
    figPotential.canvas.draw()
    for index in range(snn.getNumNeurons()):
        axbackground[index] = figPotential.canvas.copy_from_bbox(ax[index].bbox)

prvsActivity = [0] * 21
fps = FPS().start()
localfps = FPS().start()
realtimeFPS = 0
counter = 0
tbf = 0
tfor = 0
prvsDottedFlow = [0] * 8
prvsAvoidCurrents = [0] * 13
while True:
    start = time.time()

    curr = vs.readMono()
    curr = algo.contrastEnhance(curr)
    
    # calculate dense optical flow 
    # note the different parameters between old and new Farneback
    FlattenFlow = algo.calculateOpticalFlow(prvs, curr).flatten()
    meanFlattenFlow = motionFieldTemplate.meanOpticalFlow(FlattenFlow).flatten()
    
    # inner products of measured and template flows for motion compensation
    dottedFlow = motionFieldTemplate.dotWithTemplatesOpt(meanFlattenFlow, AllFlattenTemplates)
    normalizedDottedFlow = [ dotted / 4.0 for dotted in dottedFlow ]
    #movingAvgNormalizedDottedFlow = list( map(lambda x, y: x*0.05 + y*0.95, normalizedDottedFlow, prvsDottedFlow) )
    movingAvgNormalizedDottedFlow = normalizedDottedFlow
    
    # same as above, but are local for obstacle avoidance
    avoidCurrents = motionFieldTemplate.obstacleAvoidanceCurrent(meanFlattenFlow, AllFlattenTemplates)
    weightedAvoidCurrents = [ avoid * 0.23 for avoid in avoidCurrents ]
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
    activity = list( map(lambda x, y: x*0.25 + y*0.75, snn.getFirstNActivityInOrder(21), prvsActivity) )

    
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
        cv2.putText(showFrame, label[0:33], (15, 350), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255))
        cv2.putText(showFrame, "FPS={:.1f}".format(realtimeFPS), (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (5, 255, 5))
        for loc, val in enumerate(normalizedDottedFlow):
            cv2.line(showFrame, (25+loc*interval, 300), (25+loc*interval, 300-int(val*2)), color=(255, 55, 255), thickness=20)
        cv2.imshow("Dotted", showFrame)
        cv2.waitKey(1)

    if args["display_neuron"]:
        showFrame = cv2.resize(cv2.cvtColor(curr, cv2.COLOR_GRAY2BGR), (512, 512))
        interval = 40
        cv2.putText(showFrame, label[0:32], (15, 480), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255))
        cv2.putText(showFrame, "FPS={:.1f}".format(realtimeFPS), (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (5, 255, 5))
        for loc, val in enumerate(activity):
            cv2.line(showFrame, (25+(loc%8)*interval, 512-(62*(1+loc//8))), (25+(loc%8)*interval, 512-(62*(1+loc//8))-int(val)*20), color=(255, 255, 55), thickness=15)
        cv2.imshow("Neuron", showFrame)
        cv2.waitKey(1)

    if args["display_potential"]:
        potentials = potentials[-250 * snn.getNumNeurons():]
        npPotentials = np.zeros(250 * snn.getNumNeurons())
        npPotentials[-len(potentials):] = np.array(potentials)
        npPotentials = npPotentials.reshape(250, snn.getNumNeurons())
        for index in range(snn.getNumNeurons()):
            line[index].set_ydata(npPotentials[:, index])
        for index in range(snn.getNumNeurons()):
            figPotential.canvas.restore_region(axbackground[index])
        for index in range(snn.getNumNeurons()):
            ax[index].draw_artist(line[index])
        for index in range(snn.getNumNeurons()):
            figPotential.canvas.blit(ax[index].bbox)
        #figPotential.canvas.draw()
        figPotential.canvas.flush_events()

    if args["display_obstacle"]:
        showFrame = cv2.resize(cv2.cvtColor(curr, cv2.COLOR_GRAY2BGR), (512, 512))
        cv2.rectangle(showFrame, (0, 0), (510, 62), (0, int(activity[8])*255, 0), 2)
        cv2.rectangle(showFrame, (0, 0), (62, 510), (0, int(activity[9])*255, 0), 2)
        cv2.rectangle(showFrame, (448, 0), (510, 510), (0, int(activity[10])*255, 0), 2)
        cv2.rectangle(showFrame, (0, 448), (510, 510), (0, int(activity[11])*255, 0), 2)

        cv2.rectangle(showFrame, (64, 64), (446, 126), (0, int(activity[12])*255, 0), 2)
        cv2.rectangle(showFrame, (64, 64), (126, 446), (0, int(activity[13])*255, 0), 2)
        cv2.rectangle(showFrame, (384, 64), (446, 446), (0, int(activity[14])*255, 0), 2)
        cv2.rectangle(showFrame, (64, 384), (446, 446), (0, int(activity[15])*255, 0), 2)

        cv2.rectangle(showFrame, (128, 128), (382, 190), (0, int(activity[16])*255, 0), 2)
        cv2.rectangle(showFrame, (128, 128), (190, 382), (0, int(activity[17])*255, 0), 2)
        cv2.rectangle(showFrame, (320, 128), (382, 382), (0, int(activity[18])*255, 0), 2)
        cv2.rectangle(showFrame, (128, 320), (382, 382), (0, int(activity[19])*255, 0), 2)

        cv2.rectangle(showFrame, (192, 192), (318, 318), (0, int(activity[20])*255, 0), 2)
        cv2.imshow("Neuron", showFrame)
        cv2.waitKey(1)

    if args["demo_nov"]:
        if counter % 3 == 0:
            gui.displayConfig((3, 5), activity)
        counter += 1
        showFrame = cv2.resize(cv2.cvtColor(curr, cv2.COLOR_GRAY2BGR), (256, 256))
        cv2.putText(showFrame, "FPS={:.1f}".format(realtimeFPS), (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (5, 255, 5))
        cv2.imshow("Preview", showFrame)

    prvs = curr
    prvsDottedFlow = movingAvgNormalizedDottedFlow
    prvsAvoidCurrents = movingAvgWeightedAvoidCurrents
    prvsActivity = activity
    #led.turnOffAll()
    #led.turnOnConfig(3, activity)
    fps.update()
    localfps.update()
    if localfps.isPassed(30):
        localfps.stop()
        realtimeFPS = localfps.fps()
        localfps.reset()
        localfps.start()
    if not args["continuous"] and fps.isPassed(args["num_frames"]):
        break
    end = time.time()
    if args["input"]:
        time.sleep(abs(1/frameRate - (end-start)))

#led.turnOffAll()
fps.stop()
print("Elasped time: {:.3f} s".format(fps.elapsed()))
print("Approx. average FPS: {:.3f}".format(fps.fps()))
print(tbf)
print(tfor)

cv2.destroyAllWindows()
vs.stop()
