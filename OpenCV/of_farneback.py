import sys
from os.path import splitext
import cv2
import numpy as np

inFile = str( sys.argv[1] )
outFileName = splitext(inFile)[0] + ".avi"
cap = cv2.VideoCapture(inFile)
fps = int( cap.get(cv2.CAP_PROP_FPS) )
fwidth = int( cap.get(cv2.CAP_PROP_FRAME_WIDTH) )
fheight = int( cap.get(cv2.CAP_PROP_FRAME_HEIGHT) )
print("Input file: {} fps, {} pixels wide, {} pixels high".format(fps, fwidth, fheight))
print("Processing...")

BLOCK_W = 32
BLOCK_H = 32

ret, frame1 = cap.read()
prvs = cv2.cvtColor(frame1,cv2.COLOR_BGR2GRAY)
fourcc = cv2.VideoWriter_fourcc(*'MJPG')
out = cv2.VideoWriter(outFileName,fourcc, fps, (fwidth, fheight))

while(1):
    ret, frame2 = cap.read()
    if ret==True:
        #next = frame2
        next = cv2.cvtColor(frame2,cv2.COLOR_BGR2GRAY)
        flow = cv2.calcOpticalFlowFarneback(prvs, next, None,0.5, 3, 15, 3, 5, 1.2, 0)

        for y in range(0, fheight, BLOCK_H):
            for x in range(0, fwidth, BLOCK_W):
                cv2.line(frame2, (x, y), (x+int(flow[y, x, 0]), y+int(flow[y, x, 1])), ( 0, 255, 0 ), thickness=2, lineType=4, shift=0)
        out.write(frame2)
        cv2.imshow('frame2',frame2)
        prvs = next
        if cv2.waitKey(1) & 0xff == ord('q'):
            break

    else:
        break

cap.release()
out.release()
cv2.destroyAllWindows()

