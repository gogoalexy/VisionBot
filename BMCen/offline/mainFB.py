# According to the official manual, INTER_CUBIC/INTER_LINEAR interpolation is the best for enlarging videos.
import sys
import cv2
import numpy as np
from os.path import splitext
sys.path.append("../")
import visualize
import motionlib

inFile = str( sys.argv[1] )
cap = cv2.VideoCapture(inFile)
fps = int( cap.get(cv2.CAP_PROP_FPS) )
HW = tuple([int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)), int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))])
outFileName = splitext(inFile)[0] + "_FB.avi"
fourcc = cv2.VideoWriter_fourcc(*'MJPG')
out = cv2.VideoWriter(outFileName, fourcc, fps, (512, 512))

ret, previous_frame = cap.read()
prvs = cv2.cvtColor(previous_frame, cv2.COLOR_BGR2GRAY)

while(cap.isOpened()):
    ret, current_frame = cap.read()
    if ret == True:
        curr = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)
        flow = cv2.calcOpticalFlowFarneback(prvs, curr, None, 0.5, 8, 15, 3, 5, 1.2, 0)
        outframe = cv2.resize(current_frame, (512, 512), interpolation=cv2.INTER_CUBIC)
        for y in range(4, HW[0], 8):
            for x in range(4, HW[1], 8):
                cv2.line(display, (8*x, 8*y), (8*x+int(8*flow[y, x, 0]), 8*y+int(8*flow[y, x, 1])), ( 0, 255, 0 ), thickness=3, lineType=4, shift=0)
        out.write(display)
        prvs = curr
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

cap.release()
out.release()
