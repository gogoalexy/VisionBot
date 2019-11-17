import numpy as np
import cv2

canvas = np.zeros((1000, 1000, 3), dtype=np.uint8)
cv2.line(canvas, (500, 200), (500, 800), (255, 255, 255), thickness=3)
cv2.line(canvas, (200, 500), (800, 500), (255, 255, 255), thickness=3)
cv2.rectangle(canvas, (200, 200), (800, 800), (255, 255, 255), thickness=5)
cv2.line(canvas, (0, 0), (200, 200), (255, 255, 255), thickness=5)
cv2.line(canvas, (999, 0), (800, 200), (255, 255, 255), thickness=5)
cv2.line(canvas, (0, 999), (200, 800), (255, 255, 255), thickness=5)
cv2.line(canvas, (999, 999), (800, 800), (255, 255, 255), thickness=5)

inactiveColor = (80, 80, 80)
activeColor = (255, 255, 255)
#UP
cv2.arrowedLine(canvas, (270, 450), (270, 250), inactiveColor, thickness=30)
cv2.arrowedLine(canvas, (350, 450), (350, 250), inactiveColor, thickness=30)
cv2.arrowedLine(canvas, (430, 450), (430, 250), inactiveColor, thickness=30)
#DOWN
cv2.arrowedLine(canvas, (270, 250), (270, 450), inactiveColor, thickness=30)
cv2.arrowedLine(canvas, (350, 250), (350, 450), inactiveColor, thickness=30)
cv2.arrowedLine(canvas, (430, 250), (430, 450), inactiveColor, thickness=30)
#LEFT
cv2.arrowedLine(canvas, (550, 270), (750, 270), inactiveColor, thickness=30)
cv2.arrowedLine(canvas, (550, 350), (750, 350), inactiveColor, thickness=30)
cv2.arrowedLine(canvas, (550, 430), (750, 430), inactiveColor, thickness=30)
#RIGHT
cv2.arrowedLine(canvas, (750, 270), (550, 270), inactiveColor, thickness=30)
cv2.arrowedLine(canvas, (750, 350), (550, 350), inactiveColor, thickness=30)
cv2.arrowedLine(canvas, (750, 430), (550, 430), inactiveColor, thickness=30)
#ZOOMIN
cv2.arrowedLine(canvas, (330, 630), (230, 530), inactiveColor, thickness=30)
cv2.arrowedLine(canvas, (330, 670), (230, 770), inactiveColor, thickness=30)
cv2.arrowedLine(canvas, (370, 630), (470, 530), inactiveColor, thickness=30)
cv2.arrowedLine(canvas, (370, 670), (470, 770), inactiveColor, thickness=30)
#ZOOMOUT
cv2.arrowedLine(canvas, (230, 530), (330, 630), inactiveColor, thickness=30)
cv2.arrowedLine(canvas, (230, 770), (330, 670), inactiveColor, thickness=30)
cv2.arrowedLine(canvas, (470, 530), (370, 630), inactiveColor, thickness=30)
cv2.arrowedLine(canvas, (470, 770), (370, 670), inactiveColor, thickness=30)
#CW
cv2.drawMarker(canvas, (550, 650), inactiveColor, cv2.MARKER_TRIANGLE_UP, markerSize=30, thickness=20)
cv2.drawMarker(canvas, (750, 650), inactiveColor, cv2.MARKER_TRIANGLE_DOWN, markerSize=30, thickness=20)
#CCW
cv2.drawMarker(canvas, (550, 650), inactiveColor, cv2.MARKER_TRIANGLE_DOWN, markerSize=30, thickness=20)
cv2.drawMarker(canvas, (750, 650), inactiveColor, cv2.MARKER_TRIANGLE_UP, markerSize=30, thickness=20)
cv2.circle(canvas, (650, 650), 100, inactiveColor, thickness=20)

cv2.imshow("Motion", canvas)
cv2.waitKey(2000)
cv2.imwrite("MotionBackground.jpg", canvas)

cv2.destroyAllWindows()
