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
        self.arrows = [upArrow, downArrow, leftArrow, rightArrow, zoominArrow, zoomoutArrow, cwArrow, ccwArrow]
        frontSide = np.array([[0, 0], [200, 200], [824, 200], [1023, 0]])
        rearSide = np.array([[1023, 1023], [824, 824], [200, 824], [0, 1023]])
        leftSide = np.array([[0, 0], [200, 200], [200, 824], [0, 1023]])
        rightSide = np.array([[1023, 0], [824, 200], [824, 824], [1023, 1023]])
        self.sides = [frontSide, rearSide, leftSide, rightSide]
        self.inactiveColor = (80, 80, 80)
        self.activeColor = (255, 255, 255)
        self.obstacleColor = (20, 200, 250)
        self.background = 255 * np.ones((1024, 1024, 3), dtype=np.uint8)
        drone = cv2.imread("test/drone.jpg")
        roi = cv2.resize(drone, (480, 320))
        self.background[352:672, 272:752] = roi
        self.canvas = np.zeros((1000, 1000, 3), dtype=np.uint8)
        cv2.line(self.canvas, (500, 0), (500, 999), (255, 255, 255), thickness=3)
        cv2.line(self.canvas, (0, 500), (999, 500), (255, 255, 255), thickness=3)
    
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
        cv2.waitKey(1)
    
    def showMotion(self, threshold, config):
        motion = self.canvas.copy()
        for index, activity in enumerate(config, start=0):
            if index > 5:
                break
            if activity > threshold:
                motion = self.drawArrows(motion, self.arrows[index], self.activeColor)
            else:
                motion = self.drawArrows(motion, self.arrows[index], self.inactiveColor)
        if config[6] > threshold:
            cv2.drawMarker(motion, (580, 750), self.activeColor, cv2.MARKER_TRIANGLE_UP, markerSize=50, thickness=20)
            cv2.drawMarker(motion, (920, 750), self.activeColor, cv2.MARKER_TRIANGLE_DOWN, markerSize=50, thickness=20)
        else:
            cv2.drawMarker(motion, (580, 750), self.inactiveColor, cv2.MARKER_TRIANGLE_UP, markerSize=50, thickness=20)
            cv2.drawMarker(motion, (920, 750), self.inactiveColor, cv2.MARKER_TRIANGLE_DOWN, markerSize=50, thickness=20)
        if config[7] > threshold:
            cv2.drawMarker(motion, (580, 750), self.activeColor, cv2.MARKER_TRIANGLE_DOWN, markerSize=50, thickness=20)
            cv2.drawMarker(motion, (920, 750), self.activeColor, cv2.MARKER_TRIANGLE_UP, markerSize=50, thickness=20)
        else:
            cv2.drawMarker(motion, (580, 750), self.inactiveColor, cv2.MARKER_TRIANGLE_DOWN, markerSize=50, thickness=20)
            cv2.drawMarker(motion, (920, 750), self.inactiveColor, cv2.MARKER_TRIANGLE_UP, markerSize=50, thickness=20)
        if config[6] > threshold or config[7] > threshold:
            cv2.circle(motion, (750, 750), 170, self.activeColor, thickness=20)
        else:
            cv2.circle(motion, (750, 750), 170, self.inactiveColor, thickness=20)

        cv2.imshow("Motion", motion)
        cv2.waitKey(1)
    # front, rear, left, right
    def displayConfig(self, thresholds, config):
        self.showMotion(thresholds[0], config[0:8])
        self.showObstacle(thresholds[1], config[8:12])
            