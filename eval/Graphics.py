import numpy as np
import cv2

class Graphics():


    def __init__(self):
        upArrow = np.array([ ( (87, 300), (87, 50) ), ( (174, 300), (174, 50) ), ( (261, 300), (261, 50) ) ])
        downArrow = np.array([ ( (87, 400), (87, 650) ), ( (174, 400), (174, 650) ), ( (261, 400), (261, 650) ) ])
        leftArrow = np.array([ ( (1000, 437), (750, 437) ), ( (1000, 524), (750, 524) ), ( (1000, 611), (750, 611) ) ])
        rightArrow = np.array([ ( (750, 87), (1000, 87) ), ( (750, 174), (1000, 174) ), ( (750, 261), (1000, 261) ) ])
        zoominArrow = np.array([ ( (500, 150), (400, 50) ), ( (500, 200), (400, 300) ), ( (550, 150), (650, 50) ), ( (550, 200), (650, 300) ), ( (500, 175), (375, 175) ), ( (550, 175), (675, 175) ), ( (525, 150), (525, 25) ), ( (525, 200), (525, 325) ) ])
        zoomoutArrow = np.array([ ( (400, 400), (475, 475) ), ( (400, 650), (475, 575) ), ( (650, 400), (575, 475) ), ( (650, 650), (575, 575) ), ( (375, 525), (475, 525) ), ( (675, 525), (575, 525) ), ( (525, 375), (525, 475) ), ( (525, 675), (525, 575) ) ])
        cwArrow = np.array( [  ] )
        ccwArrow = np.array( [  ] )
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
        #obstacle = self.blank.copy()
        for index in range(8):
            if config[index] > thresholds[0]:
                motion = self.drawArrows(motion, self.arrows[index], self.activeColor)
        #for index in range(8, 12):
        #    if config[index] > thresholds[1]:
        #        obstacle = self.drawObstacles(obstacle, self.arrows[index], self.activeColor)
        
        cv2.imshow("Motion", motion)
        #cv2.imshow("Obstacle", obstacle)
        cv2.waitKey(10)
