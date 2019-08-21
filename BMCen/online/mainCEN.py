import sys
import cv2
import time
import ctypes
import numpy as np
import numpy.ctypeslib as npct
from os.path import splitext
sys.path.append("../")
import visualize

ucharPtr = npct.ndpointer(dtype=np.uint8, flags='CONTIGUOUS')
motionlib = ctypes.cdll.LoadLibrary("../build/libmotion.so")
motionlib.get_BM.restype = None
motionlib.get_BM.argtypes = [ucharPtr, ucharPtr, npct.ndpointer(dtype=np.int32)]
motionlib.get_CEN.restype = None
motionlib.get_CEN.argtypes = [ucharPtr, ucharPtr, npct.ndpointer(dtype=np.int32), npct.ndpointer(dtype=np.int32), npct.ndpointer(dtype=np.float64)]

HW = tuple([64, 64])
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, HW[1])
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, HW[0])
fps = int( cap.get(cv2.CAP_PROP_FPS) )

ret, previous_frame = cap.read()
prvs = cv2.cvtColor(previous_frame, cv2.COLOR_BGR2GRAY)
prvsBinMass = np.zeros((64, 64), dtype=np.int32)
currBinMass = np.zeros((64, 64), dtype=np.int32)

framecount = 0
mfps = 0
cfps = 0.01

while(cap.isOpened()):
    start = time.time()
    framecount += 1
    CEN = np.zeros((8, 8, 2))
    ret, current_frame = cap.read()
    if ret == True:
        curr = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)
        motionlib.get_CEN(curr, prvs, currBinMass, prvsBinMass, CEN)
        outframe = cv2.resize(current_frame, (512, 512))
        if framecount % 10 == 0:
            mfps = int(10/cfps)
            cfps = 0.01
        cv2.putText(outframe, str(mfps), (30, 80), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 255, 0))
        cv2.imshow("Centroid", visualize.drawFlowArrow(outframe, CEN))
        prvs = curr
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break
    end = time.time()
    cfps  += (end - start);

cap.release()
cv2.destroyAllWindows()
