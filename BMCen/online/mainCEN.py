import sys
import cv2
import time
import numpy as np
from os.path import splitext
sys.path.append("../")
import visualize
import motionlib

HW = tuple([64, 64])
cap = cv2.VideoCapture(0)
src.set(cv2.CAP_PROP_FRAME_WIDTH, HW[1])
src.set(cv2.CAP_PROP_FRAME_HEIGHT, HW[0])
fps = int( cap.get(cv2.CAP_PROP_FPS) )

ret, previous_frame = cap.read()
prvs = cv2.cvtColor(previous_frame, cv2.COLOR_BGR2GRAY)
prvsBinMass = np.zeros((64, 64))

while(cap.isOpened()):
    start = time.time()
    CEN = np.zeros((8, 8, 2))
    ret, current_frame = cap.read()
    if ret == True:
        curr = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)
        prvsBinMass = motion.getCEN(prvs, curr, prvsBinMass, CEN)
        outframe = visualize.drawGrids(current_frame, 0, 63, 8)
        cv2.imshow("Centroid", visualize.drawFlowArrow(outframe, CEN))
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else: 
        break
    end = time.time()
    fps  = 1 / (end - start);
    print(fps)
 
cap.release()
cv2.destroyAllWindows()
