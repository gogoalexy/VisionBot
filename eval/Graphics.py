import numpy as np
import cv2

class Graphics():


    def __init__(self):
        upArrow = np.array([ ( (80, 400), (80, 100) ), ( (240, 400), (240, 100) ), ( (400, 400), (400, 100) ) ])
        downArrow = np.array([ ( (80, 100), (80, 400) ), ( (240, 100), (240, 400) ), ( (400, 100), (400, 400) ) ])
        leftArrow = np.array([ ( (580, 80), (900, 80) ), ( (580, 240), (900, 240) ), ( (580, 400), (900, 400) ) ])
        rightArrow = np.array([ ( (900, 80), (580, 80) ), ( (900, 240), (580, 240) ), ( (900, 400), (580, 400) ) ])
        zoominArrow = np.array([ ( (225, 725), (50, 550) ), ((225, 775), (50, 950)  ), ( (275, 725), (450, 550) ), ((275, 775), (450, 950)  ) ])
        zoomoutArrow = np.array([ ((50, 550), (225, 725)  ), ( (50, 950), (225, 775) ), ( (450, 550), (275, 725) ), ((450, 950), (275, 775)  ) ])
        cwArrow = np.array( [  ] )
        ccwArrow = np.array( [  ] )
        self.arrows = [cwArrow, ccwArrow, zoominArrow, zoomoutArrow, downArrow, upArrow, rightArrow, leftArrow]
        frontSide = np.array([[0, 0], [200, 200], [600, 200], [799, 0]])
        rearSide = np.array([[799, 799], [600, 600], [200, 600], [0, 799]])
        leftSide = np.array([[0, 0], [200, 200], [200, 600], [0, 799]])
        rightSide = np.array([[799, 0], [600, 200], [600, 600], [799, 799]])
        self.sides = [frontSide, rearSide, leftSide, rightSide]
        self.inactiveColor = (80, 80, 80)
        self.activeColor = (255, 255, 255)
        self.obstacleColor = (20, 200, 250)
        self.background = cv2.imread("ObstacleBackground.jpg")
        self.canvas = cv2.imread("MotionBackground.jpg")

    def drawArrows(self, image, positions, color):
        for index in range(positions.shape[0]):
            cv2.arrowedLine(image, tuple(positions[index][0]), tuple(positions[index][1]), color, thickness=30)
        return image

    def showObstacle(self, threshold, config):
        obstacle = self.background.copy()
        for index, activity in enumerate(config, start=0):
            if activity > threshold:
                cv2.fillConvexPoly(obstacle, self.sides[index], self.obstacleColor)
        cv2.imshow("Obstacle", obstacle)

    def showMotion(self, threshold, config):
        motion = self.canvas.copy()
        for index in range(8):
            if config[index] > threshold:
                motion = self.drawArrows(motion, self.arrows[index], self.activeColor)

        if config[6] > threshold:
            cv2.drawMarker(motion, (580, 750), self.activeColor, cv2.MARKER_TRIANGLE_UP, markerSize=50, thickness=20)
            cv2.drawMarker(motion, (920, 750), self.activeColor, cv2.MARKER_TRIANGLE_DOWN, markerSize=50, thickness=20)

        if config[7] > threshold:
            cv2.drawMarker(motion, (580, 750), self.activeColor, cv2.MARKER_TRIANGLE_DOWN, markerSize=50, thickness=20)
            cv2.drawMarker(motion, (920, 750), self.activeColor, cv2.MARKER_TRIANGLE_UP, markerSize=50, thickness=20)

        if config[6] > threshold or config[7] > threshold:
            cv2.circle(motion, (750, 750), 170, self.activeColor, thickness=20)

        cv2.imshow("Motion", motion)

    # front, rear, left, right
    def displayConfig(self, thresholds, config):
        self.showMotion(thresholds[0], config[0:8])
        self.showObstacle(thresholds[1], config[8:12])
        cv2.waitKey(10)
