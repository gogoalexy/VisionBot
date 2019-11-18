import numpy as np
import cv2

class Graphics():


    def __init__(self):
        upArrow = np.array([ ( (270, 450), (270, 250) ), ( (350, 450), (350, 250) ), ( (430, 450), (430, 250) ) ])
        downArrow = np.array([ ( (270, 250), (270, 450) ), ( (350, 250), (350, 450) ), ( (430, 250), (430, 450) ) ])
        rightArrow = np.array([ ( (550, 270), (750, 270) ), ( (550, 350), (750, 350) ), ( (550, 430), (750, 430) ) ])
        leftArrow = np.array([ ( (750, 270), (550, 270) ), ( (750, 350), (550, 350) ), ( (750, 430), (550, 430) ) ])
        zoominArrow = np.array([ ( (330, 630), (230, 530) ), ((330, 670), (230, 770)  ), ( (370, 630), (470, 530) ), ((370, 670), (470, 770)  ) ])
        zoomoutArrow = np.array([ ((230, 530), (330, 630)  ), ( (230, 770), (330, 670) ), ( (470, 530), (370, 630) ), ((470, 770), (370, 670)  ) ])
        cwArrow = np.array( [  ] )
        ccwArrow = np.array( [  ] )
        frontSide = np.array([[0, 0], [200, 200], [800, 200], [999, 0]])
        rearSide = np.array([[999, 999], [800, 800], [200, 800], [0, 999]])
        leftSide = np.array([[0, 0], [200, 200], [200, 800], [0, 999]])
        rightSide = np.array([[999, 0], [800, 200], [800, 800], [999, 999]])
        self.arrows = [cwArrow, ccwArrow, zoominArrow, zoomoutArrow, downArrow, upArrow, rightArrow, leftArrow, frontSide, rearSide, leftSide, rightSide]
        self.inactiveColor = (80, 80, 80)
        self.activeColor = (255, 255, 255)
        self.obstacleColor = (20, 200, 250)
        self.canvas = cv2.imread("MotionBackground.jpg")

    def drawArrows(self, image, positions, color):
        for index in range(positions.shape[0]):
            cv2.arrowedLine(image, tuple(positions[index][0]), tuple(positions[index][1]), color, thickness=30)
        return image

    # front, rear, left, right
    def displayConfig(self, thresholds, config):
        motion = self.canvas.copy()
        for index in range(8):
            if config[index] > thresholds[0]:
                motion = self.drawArrows(motion, self.arrows[index], self.activeColor)

        if config[6] > thresholds[0]:
            cv2.drawMarker(motion, (550, 650), self.activeColor, cv2.MARKER_TRIANGLE_UP, markerSize=50, thickness=20)
            cv2.drawMarker(motion, (750, 650), self.activeColor, cv2.MARKER_TRIANGLE_DOWN, markerSize=50, thickness=20)

        if config[7] > thresholds[0]:
            cv2.drawMarker(motion, (550, 650), self.activeColor, cv2.MARKER_TRIANGLE_DOWN, markerSize=50, thickness=20)
            cv2.drawMarker(motion, (750, 650), self.activeColor, cv2.MARKER_TRIANGLE_UP, markerSize=50, thickness=20)

        if config[6] > thresholds[0] or config[7] > thresholds[0]:
            cv2.circle(motion, (650, 650), 100, self.activeColor, thickness=20)

        for index in range(8, 12):
            if config[index] > thresholds[1]:
                cv2.fillConvexPoly(motion, self.arrows[index], self.obstacleColor)

        cv2.imshow("Motion", motion)
        cv2.waitKey(10)
