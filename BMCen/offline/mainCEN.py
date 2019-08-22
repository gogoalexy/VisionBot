import sys
import cv2
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

inFile = str( sys.argv[1] )
cap = cv2.VideoCapture(inFile)
fps = int( cap.get(cv2.CAP_PROP_FPS) )
HW = tuple([int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)), int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))])
outFileName = splitext(inFile)[0] + "_CEN.avi"
fourcc = cv2.VideoWriter_fourcc(*'MJPG')
out = cv2.VideoWriter(outFileName, fourcc, fps, (512, 512))

ret, previous_frame = cap.read()
prvs = cv2.cvtColor(previous_frame, cv2.COLOR_BGR2GRAY)
prvsBinMass = np.zeros((64, 64), dtype=np.int32)
currBinMass = np.zeros((64, 64), dtype=np.int32)

while(cap.isOpened()):
    CEN = np.zeros((8, 8, 2))
    ret, current_frame = cap.read()
    if ret == True:
        curr = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)
        motionlib.get_CEN(curr, prvs, currBinMass, prvsBinMass, CEN)
        outframe = cv2.resize(current_frame, (512, 512), interpolation=cv2.INTER_CUBIC)
        out.write(visualize.drawFlowArrow(visualize.drawGrids(outframe, 0, 512, 64), CEN))
        prvs = curr
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

cap.release()
out.release()

