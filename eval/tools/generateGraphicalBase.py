import numpy as np
import cv2

front = np.array([[0, 0], [200, 200], [600, 200], [799, 0]])
rear = np.array([[799, 799], [600, 600], [200, 600], [0, 799]])
left = np.array([[0, 0], [200, 200], [200, 600], [0, 799]])
right = np.array([[799, 0], [600, 200], [600, 600], [799, 799]])

background = 255 * np.ones((800, 800, 3), dtype=np.uint8)
drone = cv2.imread("../test/drone.jpg")
roi = cv2.resize(drone, (480, 320))
background[240:560, 160:640] = roi
cv2.rectangle(background, (180, 200), (605, 600), (0, 0, 0), thickness=5)
cv2.line(background, (0, 0), (180, 200), (0, 0, 0), thickness=5)
cv2.line(background, (799, 0), (605, 200), (0, 0, 0), thickness=5)
cv2.line(background, (0, 799), (180, 600), (0, 0, 0), thickness=5)
cv2.line(background, (799, 799), (605, 600), (0, 0, 0), thickness=5)

cv2.imshow("Obstacle", background)
cv2.imwrite("ObstacleBackground.jpg", background)

canvas = np.zeros((1000, 1000, 3), dtype=np.uint8)
cv2.line(canvas, (500, 0), (500, 999), (255, 255, 255), thickness=3)
cv2.line(canvas, (0, 500), (999, 500), (255, 255, 255), thickness=3)

inactiveColor = (80, 80, 80)
activeColor = (255, 255, 255)
#UP
cv2.arrowedLine(canvas, (80, 400), (80, 100), inactiveColor, thickness=30)
cv2.arrowedLine(canvas, (240, 400), (240, 100), inactiveColor, thickness=30)
cv2.arrowedLine(canvas, (400, 400), (400, 100), inactiveColor, thickness=30)
#DOWN
cv2.arrowedLine(canvas, (80, 100), (80, 400), inactiveColor, thickness=30)
cv2.arrowedLine(canvas, (240, 100), (240, 400), inactiveColor, thickness=30)
cv2.arrowedLine(canvas, (400, 100), (400, 400), inactiveColor, thickness=30)
#LEFT
cv2.arrowedLine(canvas, (580, 80), (900, 80), inactiveColor, thickness=30)
cv2.arrowedLine(canvas, (580, 240), (900, 240), inactiveColor, thickness=30)
cv2.arrowedLine(canvas, (580, 400), (900, 400), inactiveColor, thickness=30)
#RIGHT
cv2.arrowedLine(canvas, (900, 80), (580, 80), inactiveColor, thickness=30)
cv2.arrowedLine(canvas, (900, 240), (580, 240), inactiveColor, thickness=30)
cv2.arrowedLine(canvas, (900, 400), (580, 400), inactiveColor, thickness=30)
#ZOOMIN
cv2.arrowedLine(canvas, (225, 725), (50, 550), inactiveColor, thickness=30)
cv2.arrowedLine(canvas, (225, 775), (50, 950), inactiveColor, thickness=30)
cv2.arrowedLine(canvas, (275, 725), (450, 550), inactiveColor, thickness=30)
cv2.arrowedLine(canvas, (275, 775), (450, 950), inactiveColor, thickness=30)
#ZOOMOUT
cv2.arrowedLine(canvas, (50, 550), (225, 725), inactiveColor, thickness=30)
cv2.arrowedLine(canvas, (50, 950), (225, 775), inactiveColor, thickness=30)
cv2.arrowedLine(canvas, (450, 550), (275, 725), inactiveColor, thickness=30)
cv2.arrowedLine(canvas, (450, 950), (275, 775), inactiveColor, thickness=30)
#CW
cv2.drawMarker(canvas, (580, 750), inactiveColor, cv2.MARKER_TRIANGLE_UP, markerSize=50, thickness=20)
cv2.drawMarker(canvas, (920, 750), inactiveColor, cv2.MARKER_TRIANGLE_DOWN, markerSize=50, thickness=20)
#CCW
cv2.drawMarker(canvas, (580, 750), inactiveColor, cv2.MARKER_TRIANGLE_DOWN, markerSize=50, thickness=20)
cv2.drawMarker(canvas, (920, 750), inactiveColor, cv2.MARKER_TRIANGLE_UP, markerSize=50, thickness=20)
cv2.circle(canvas, (750, 750), 170, inactiveColor, thickness=20)

cv2.imshow("Motion", canvas)
cv2.waitKey(0)
cv2.imwrite("MotionBackground.jpg", canvas)

cv2.destroyAllWindows()
