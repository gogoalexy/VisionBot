import numpy as np
import cv2

canvas = np.zeros((700, 1050, 3), dtype=np.uint8)
cv2.line(canvas, (350, 0), (350, 699), (255, 255, 255), thickness=3)
cv2.line(canvas, (700, 0), (700, 699), (255, 255, 255), thickness=3)
cv2.line(canvas, (0, 350), (1049, 350), (255, 255, 255), thickness=3)

inactiveColor = (80, 80, 80)
activeColor = (255, 255, 255)
#UP
cv2.arrowedLine(canvas, (87, 300), (87, 50), inactiveColor, thickness=20)
cv2.arrowedLine(canvas, (174, 300), (174, 50), inactiveColor, thickness=20)
cv2.arrowedLine(canvas, (261, 300), (261, 50), inactiveColor, thickness=20)
#DOWN
cv2.arrowedLine(canvas, (87, 400), (87, 650), inactiveColor, thickness=20)
cv2.arrowedLine(canvas, (174, 400), (174, 650), inactiveColor, thickness=20)
cv2.arrowedLine(canvas, (261, 400), (261, 650), inactiveColor, thickness=20)
#LEFT
cv2.arrowedLine(canvas, (750, 87), (1000, 87), inactiveColor, thickness=20)
cv2.arrowedLine(canvas, (750, 174), (1000, 174), inactiveColor, thickness=20)
cv2.arrowedLine(canvas, (750, 261), (1000, 261), inactiveColor, thickness=20)
#RIGHT
cv2.arrowedLine(canvas, (1000, 437), (750, 437), inactiveColor, thickness=20)
cv2.arrowedLine(canvas, (1000, 524), (750, 524), inactiveColor, thickness=20)
cv2.arrowedLine(canvas, (1000, 611), (750, 611), inactiveColor, thickness=20)
#ZOOMIN
cv2.arrowedLine(canvas, (500, 150), (400, 50), inactiveColor, thickness=20)
cv2.arrowedLine(canvas, (500, 200), (400, 300), inactiveColor, thickness=20)
cv2.arrowedLine(canvas, (550, 150), (650, 50), inactiveColor, thickness=20)
cv2.arrowedLine(canvas, (550, 200), (650, 300), inactiveColor, thickness=20)
cv2.arrowedLine(canvas, (500, 175), (375, 175), inactiveColor, thickness=20)
cv2.arrowedLine(canvas, (550, 175), (675, 175), inactiveColor, thickness=20)
cv2.arrowedLine(canvas, (525, 150), (525, 25), inactiveColor, thickness=20)
cv2.arrowedLine(canvas, (525, 200), (525, 325), inactiveColor, thickness=20)
#ZOOMOUT
cv2.arrowedLine(canvas, (400, 400), (475, 475), inactiveColor, thickness=20)
cv2.arrowedLine(canvas, (400, 650), (475, 575), inactiveColor, thickness=20)
cv2.arrowedLine(canvas, (650, 400), (575, 475), inactiveColor, thickness=20)
cv2.arrowedLine(canvas, (650, 650), (575, 575), inactiveColor, thickness=20)
cv2.arrowedLine(canvas, (375, 525), (475, 525), inactiveColor, thickness=20)
cv2.arrowedLine(canvas, (675, 525), (575, 525), inactiveColor, thickness=20)
cv2.arrowedLine(canvas, (525, 375), (525, 475), inactiveColor, thickness=20)
cv2.arrowedLine(canvas, (525, 675), (525, 575), inactiveColor, thickness=20)

cv2.imshow("Motion", canvas)
cv2.waitKey(0)
cv2.imwrite("MotionBackground.jpg", canvas)

cv2.destroyAllWindows()
