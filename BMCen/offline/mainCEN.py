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
outFileName = splitext(inFile)[0] + "_CEN.mp4"
fourcc = cv2.VideoWriter_fourcc(*'MJPG')
out = cv2.VideoWriter(outFileName, fourcc, fps, HW)

ret, previous_frame = cap.read()
prvs = cv2.cvtColor(previous_frame, cv2.COLOR_BGR2GRAY)
prvsBinMass = np.zeros((64, 64))

while(cap.isOpened()):
    CEN = np.zeros((8, 8, 2))
    ret, current_frame = cap.read()
    if ret == True:
        curr = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)
        prvsBinMass = motion.getCEN(prvs, curr, prvsBinMass, CEN)
        outframe = visualize.drawGrids(current_frame, 0, 63, 8)
        out.write(visualize.drawFlowArrow(outframe, CEN))
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else: 
        break
 
cap.release()
out.release()

