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
cap.set(cv2.CAP_PROP_FRAME_WIDTH, HW[1])
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, HW[0])
fps = int( cap.get(cv2.CAP_PROP_FPS) )

ret, previous_frame = cap.read()
prvs = cv2.cvtColor(previous_frame, cv2.COLOR_BGR2GRAY)

while(cap.isOpened()):
    start = time.time()
    ret, current_frame = cap.read()
    if ret == True:
        curr = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)
        flow = cv2.calcOpticalFlowFarneback(prvs, curr, None, 0.5, 8, 15, 3, 5, 1.2, 0)
        for y in range(4, HW[0], 8):
            for x in range(4, HW[1], 8):
                cv2.line(current_frame, (x, y), (x+int(flow[y, x, 0]), y+int(flow[y, x, 1])), ( 0, 255, 0 ), thickness=2, lineType=4, shift=0)
        cv2.imshow("Farneback", cv2.resize(current_frame, (256, 256)))
        prvs = curr
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break
    end = time.time()
    fps  = 1 / (end - start);
    print(fps)

cap.release()
cv2.destroyAllWindows()
