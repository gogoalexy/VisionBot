import sys
import cv2
import time
import numpy as np
import numpy.ctypeslib as npct
import ctypes
from os.path import splitext
sys.path.append("../")
import visualize

ucharPtr = npct.ndpointer(dtype=np.uint8, flags='CONTIGUOUS')
motionlib = ctypes.cdll.LoadLibrary("../build/libmotion.so")
motionlib.get_BM.restype = None
motionlib.get_BM.argtypes = [ucharPtr, ucharPtr, npct.ndpointer(dtype=np.int32)]
motionlib.get_CEN.restype = None
motionlib.get_CEN.argtypes = [ucharPtr, npct.ndpointer(dtype=np.int32), npct.ndpointer(dtype=np.int32), npct.ndpointer(dtype=np.float64)]

HW = tuple([64, 64])
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, HW[1])
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, HW[0])
fps = int( cap.get(cv2.CAP_PROP_FPS) )

ret, previous_frame = cap.read()
prvs = cv2.cvtColor(previous_frame, cv2.COLOR_BGR2GRAY)
prvsBinMass = np.zeros((64, 64), dtype=np.int32)
currBinMass = np.zeros((64, 64), dtype=np.int32)

while(cap.isOpened()):
    start = time.time()
    CEN = np.zeros((8, 8, 2))
    ret, current_frame = cap.read()
    if ret == True:
        curr = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)
        diff = cv2.absdiff(curr, prvs)
        #tmpimg = np.asarray(diff, dtype=np.uint8, order='C')
        #tmpimg = tmpimg.ctypes.data_as(ctypes.c_char_p)
        #print(str(tmpimg.))
        motionlib.get_CEN(diff, currBinMass, prvsBinMass, CEN)
        outframe = visualize.drawGrids(current_frame, 0, 63, 8)
        cv2.imshow("Centroid", visualize.drawFlowArrow(outframe, CEN))
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
