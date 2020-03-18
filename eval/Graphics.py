import numpy as np
import cv2
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui

class Demo():


    def __init__(self):
        upArrow = np.array([ ( (87, 300), (87, 50) ), ( (174, 300), (174, 50) ), ( (261, 300), (261, 50) ) ])
        downArrow = np.array([ ( (87, 400), (87, 650) ), ( (174, 400), (174, 650) ), ( (261, 400), (261, 650) ) ])
        rightArrow = np.array([ ( (1000, 437), (750, 437) ), ( (1000, 524), (750, 524) ), ( (1000, 611), (750, 611) ) ])
        leftArrow = np.array([ ( (750, 87), (1000, 87) ), ( (750, 174), (1000, 174) ), ( (750, 261), (1000, 261) ) ])
        zoominArrow = np.array([ ( (500, 150), (400, 50) ), ( (500, 200), (400, 300) ), ( (550, 150), (650, 50) ), ( (550, 200), (650, 300) ), ( (500, 175), (375, 175) ), ( (550, 175), (675, 175) ), ( (525, 150), (525, 25) ), ( (525, 200), (525, 325) ) ])
        zoomoutArrow = np.array([ ( (400, 400), (475, 475) ), ( (400, 650), (475, 575) ), ( (650, 400), (575, 475) ), ( (650, 650), (575, 575) ), ( (375, 525), (475, 525) ), ( (675, 525), (575, 525) ), ( (525, 375), (525, 475) ), ( (525, 675), (525, 575) ) ])
        cwArrow = np.array( [ (0, 0), (0, 0) ] )
        ccwArrow = np.array( [ (0, 0), (0, 0) ] )
        frontSide = np.array([ ( (0, 0), (249, 50) ) ])
        rearSide = np.array([ ( (249, 249), (0, 200) ) ])
        leftSide = np.array([ ( (0, 50), (50, 200) ) ])
        rightSide = np.array([ ( (200, 50), (249, 200) ) ])
        #label =  "CW  FWD DWN RT CCW  BWD  UP  LFT oUP oLFT oRT oDWN mUP mLFT mRT mDWN iUP iLFT iRT iDWN C"
        #self.arrows = [ccwArrow, cwArrow, zoominArrow, zoomoutArrow, upArrow, downArrow, rightArrow, leftArrow, frontSide, rearSide, leftSide, rightSide]
        self.arrows = [cwArrow, zoominArrow, downArrow, rightArrow, ccwArrow, zoomoutArrow, upArrow, leftArrow, frontSide, rearSide, leftSide, rightSide]
        self.inactiveColor = (80, 80, 80)
        self.activeColor = (255, 255, 255)
        self.obstacleColor = (20, 200, 250)
        self.canvas = cv2.imread("assets/MotionBackground.jpg")
        self.blank = cv2.imread("assets/ObstacleBackground.jpg")

    def mountWindowAt(self, x, y):
        cv2.imshow("Motion", self.canvas)
        cv2.moveWindow("Motion", x, y)

    def drawArrows(self, image, positions, color):
        for index in range(positions.shape[0]):
            cv2.arrowedLine(image, tuple(positions[index][0]), tuple(positions[index][1]), color, thickness=20)
        return image

    def drawObstacles(self, image, locations, color):
        for index in range(locations.shape[0]):
            cv2.rectangle(image, tuple(locations[index][0]), tuple(locations[index][1]), color, thickness=cv2.FILLED)
        return image

    # front, rear, left, right
    def displayConfig(self, thresholds, config):
        motion = self.canvas.copy()

        for index, value  in enumerate(config):
            if index == 0:
                if value > thresholds[0]:
                    cv2.circle(canvas, (1225, 175), 125, inactiveColor, thickness=20)
                    cv2.drawMarker(canvas, (1100, 175), inactiveColor, markerType=cv2.MARKER_TRIANGLE_UP, markerSize=45, thickness=20)
                    cv2.drawMarker(canvas, (1350, 175), inactiveColor, markerType=cv2.MARKER_TRIANGLE_DOWN, markerSize=45, thickness=20)
            elif index == 4:
                if value > thresholds[0]:
                    cv2.circle(canvas, (1225, 525), 125, inactiveColor, thickness=20)
                    cv2.drawMarker(canvas, (1100, 525), inactiveColor, markerType=cv2.MARKER_TRIANGLE_DOWN, markerSize=45, thickness=20)
                    cv2.drawMarker(canvas, (1350, 525), inactiveColor, markerType=cv2.MARKER_TRIANGLE_UP, markerSize=45, thickness=20)
            elif index < 8:
                if value > thresholds[0]:
                    motion = self.drawArrows(motion, self.arrows[index], self.activeColor)

        cv2.imshow("Motion", motion)


class Flow():

    def __init__(self):
        None

    def display(self, frame, flow, fps):
        showFrame = frame.copy()
        showFrame = cv2.resize(showFrame, (512, 512))
        flow = flow.reshape(8, 8, 2)
        flow = cv2.resize(flow, (512, 512), cv2.INTER_NEAREST)
        for y in range(32, 512, 64):
            for x in range(32, 512, 64):
                cv2.line(showFrame, (x, y), (x+int(5*flow[y][x][0]), y+int(5*flow[y][x][1])), (255, 255, 255), 3)
        cv2.putText(showFrame, "FPS={:.1f}".format(fps), (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (5, 255, 5))
        cv2.imshow("Flow", showFrame)

class Dot():

    def __init__(self):
        None

    def display(self, frame, label, flow, fps):
        showFrame = frame.copy()
        showFrame = cv2.resize(showFrame, (512, 512))
        interval = 40
        cv2.putText(showFrame, label[0:33], (15, 350), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255))
        cv2.putText(showFrame, "FPS={:.1f}".format(fps), (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (5, 255, 5))
        for loc, val in enumerate(flow):
            cv2.line(showFrame, (25+loc*interval, 300), (25+loc*interval, 300-int(val*2)), color=(255, 55, 255), thickness=20)
        cv2.imshow("Dotted", showFrame)


class Neuron():

    def __init__(self):
        None

    def display(self, frame, label, fps, activity):
        showFrame = frame.copy()
        showFrame = cv2.resize(showFrame, (512, 512))
        interval = 40
        cv2.putText(showFrame, label[0:32], (15, 480), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255))
        cv2.putText(showFrame, "FPS={:.1f}".format(fps), (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (5, 255, 5))
        for loc, val in enumerate(activity):
            cv2.line(showFrame, (25+(loc%8)*interval, 512-(62*(1+loc//8))), (25+(loc%8)*interval, 512-(62*(1+loc//8))-int(val)*20), color=(255, 255, 55), thickness=15)
        cv2.imshow("Neuron", showFrame)

class Potential():

    def __init__(self, numNeurons):
        potentialY = np.full(500, 255)
        self.win = pg.GraphicsWindow()
        self.win.setWindowTitle('Potentials')
        self.curvePotentials = [0] * numNeurons
        for index in range(numNeurons):
            if index % 4 == 0:
                self.win.nextRow()
            self.plotPotentials = self.win.addPlot()
            self.plotPotentials.setYRange(-10, 260, padding=0)
            self.curvePotentials[index] = self.plotPotentials.plot(potentialY)

    def display(self, potentials, numNeurons):
        npPotentials = np.zeros(500 * numNeurons)
        npPotentials[-len(potentials):] = np.array(potentials)
        npPotentials = npPotentials.reshape(500, numNeurons)
        for index in range(numNeurons):
            self.curvePotentials[index].setData(npPotentials[:, index])

class Obstacle():

    def __init__(self, threshold, saver=None):
        self.saver = saver
        self.trapezoids = []
        outUp = np.array([[2, 0], [511, 0], [446, 62], [64, 62]], np.int)
        outUp = outUp.reshape((-1, 1, 2))
        self.trapezoids.append(outUp)
        outLeft = np.array([[0, 2], [0, 511], [62, 446], [62, 64]], np.int)
        outLeft = outLeft.reshape((-1, 1, 2))
        self.trapezoids.append(outLeft)
        outRight = np.array([[511, 2], [511, 510], [448, 446], [448, 64]], np.int)
        outRight = outRight.reshape((-1, 1, 2))
        self.trapezoids.append(outRight)
        outDown = np.array([[2, 511], [510, 511], [446, 448], [64, 448]], np.int)
        outDown = outDown.reshape((-1, 1, 2))
        self.trapezoids.append(outDown)
        midUp = np.array([[64, 64], [446, 64], [384, 126], [128, 126]], np.int)
        midUp = midUp.reshape((-1, 1, 2))
        self.trapezoids.append(midUp)
        midLeft = np.array([[64, 64], [64, 446], [126, 384], [126, 128]], np.int)
        midLeft = midLeft.reshape((-1, 1, 2))
        self.trapezoids.append(midLeft)
        midRight = np.array([[446, 64], [446, 446], [384, 382], [384, 128]], np.int)
        midRight = midRight.reshape((-1, 1, 2))
        self.trapezoids.append(midRight)
        midDown = np.array([[64, 446], [446, 446], [382, 384], [128, 384]], np.int)
        midDown = midDown.reshape((-1, 1, 2))
        self.trapezoids.append(midDown)
        inUp = np.array([[128, 128], [382, 128], [318, 190], [192, 190]], np.int)
        inUp = inUp.reshape((-1, 1, 2))
        self.trapezoids.append(inUp)
        inLeft = np.array([[128, 128], [128, 382], [190, 318], [190, 192]], np.int)
        inLeft = inLeft.reshape((-1, 1, 2))
        self.trapezoids.append(inLeft)
        inRight = np.array([[382, 128], [382, 382], [320, 318], [320, 192]], np.int)
        inRight = inRight.reshape((-1, 1, 2))
        self.trapezoids.append(inRight)
        inDown = np.array([[128, 382], [382, 382], [318, 320], [192, 320]], np.int)
        inDown = inDown.reshape((-1, 1, 2))
        self.trapezoids.append(inDown)

        self.threshold = threshold

    def display(self, frame, activity, fps):
        showFrame = frame.copy()
        showFrame = cv2.resize(showFrame, (512, 512))
        
        cv2.line(showFrame, (0, 0), (192, 192), (0, 0, 0), 2)
        cv2.line(showFrame, (320, 320), (512, 512), (0, 0, 0), 2)
        cv2.line(showFrame, (0, 512), (192, 320), (0, 0, 0), 2)
        cv2.line(showFrame, (512, 0), (320, 192), (0, 0, 0), 2)
        cv2.rectangle(showFrame, (64, 64), (448, 448), (0, 0, 0), 2)
        cv2.rectangle(showFrame, (128, 128), (384, 384), (0, 0, 0), 2)
        cv2.rectangle(showFrame, (192, 192), (320, 320), (0, 0, 0), 2)
        
        for loc, val in enumerate(self.trapezoids):
            if activity[loc + 8] > self.threshold:
                cv2.polylines(showFrame, [val], True, (0, 255, 0), 12)

        if activity[20] > self.threshold:
            cv2.rectangle(showFrame, (192, 192), (318, 318), (0, 255, 0), 12)

        if self.saver is not None:
            self.saver.write(showFrame)
        else:
            cv2.putText(showFrame, "FPS={:.1f}".format(fps), (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (5, 255, 5))
        cv2.imshow("Obstacles", showFrame)

