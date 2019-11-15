import numpy as np
import cv2

front = np.array([[0, 0], [200, 200], [824, 200], [1023, 0]])
rear = np.array([[1023, 1023], [824, 824], [200, 824], [0, 1023]])
left = np.array([[0, 0], [200, 200], [200, 824], [0, 1023]])
right = np.array([[1023, 0], [824, 200], [824, 824], [1023, 1023]])

background = 255 * np.ones((1024, 1024, 3), dtype=np.uint8)
drone = cv2.imread("drone.jpg")
roi = cv2.resize(drone, (480, 320))
background[352:672, 272:752] = roi
out = cv2.fillConvexPoly(background, right, (20, 200, 250))
cv2.imshow("Obstacle", out)

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
cv2.drawMarker(canvas, (580, 750), activeColor, cv2.MARKER_TRIANGLE_DOWN, markerSize=50, thickness=20)
cv2.drawMarker(canvas, (920, 750), activeColor, cv2.MARKER_TRIANGLE_UP, markerSize=50, thickness=20)
cv2.circle(canvas, (750, 750), 170, activeColor, thickness=20)

cv2.imshow("Motion", canvas)
cv2.waitKey(0)

cv2.destroyAllWindows()