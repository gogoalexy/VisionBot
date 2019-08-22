import sys
import cv2
import time
import numpy as np
from os.path import splitext
sys.path.append("../")
import visualize

HW = tuple([64, 64])
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, HW[1])
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, HW[0])
fps = int( cap.get(cv2.CAP_PROP_FPS) )

ret, previous_frame = cap.read()
prvs = cv2.cvtColor(previous_frame, cv2.COLOR_BGR2GRAY)

framecount = 0
mfps = 0
cfps = 0.01

while(cap.isOpened()):
    start = time.time()
    framecount += 1
    ret, current_frame = cap.read()
    if ret == True:
        curr = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)
        flow = cv2.calcOpticalFlowFarneback(prvs, curr, None, 0.5, 8, 15, 3, 5, 1.2, 0)
        outframe = cv2.resize(current_frame, (512, 512))
        for y in range(4, HW[0], 8):
            for x in range(4, HW[1], 8):
                cv2.line(outframe, (8*x, 8*y), (8*(x+int(flow[y, x, 0])), 8*(y+int(flow[y, x, 1]))), ( 0, 255, 0 ), thickness=2, lineType=4, shift=0)
        if framecount % 10 == 0:
            mfps = int(10/cfps)
            cfps = 0.01
        cv2.putText(outframe, str(mfps), (30, 80), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 255, 0))
        cv2.imshow("Farneback", outframe)
        prvs = curr
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break
    end = time.time()
    cfps  += (end - start);

cap.release()
cv2.destroyAllWindows()
