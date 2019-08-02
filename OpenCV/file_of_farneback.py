import sys
from os.path import splitext
import cv2
import numpy as np

inFile = str( sys.argv[1] )
outFile = open( splitext(inFile)[0] + ".flow", 'w' )
cap = cv2.VideoCapture(inFile)
fps = int( cap.get(cv2.CAP_PROP_FPS) )
fwidth = int( cap.get(cv2.CAP_PROP_FRAME_WIDTH) )
fheight = int( cap.get(cv2.CAP_PROP_FRAME_HEIGHT) )
print("Input file: {} fps, {} pixels wide, {} pixels high".format(fps, fwidth, fheight))
print("Processing...")

ret, frame1 = cap.read()
prvs = cv2.cvtColor(frame1, cv2.COLOR_RGB2GRAY)

while(1):
    ret, frame2 = cap.read()
    if ret==True:
        next = cv2.cvtColor(frame2, cv2.COLOR_RGB2GRAY)
        flow = cv2.calcOpticalFlowFarneback(prvs, next, None, 0.5, 3, 15, 3, 5, 1.2, 0)

        for y in range(0, fheight):
            for x in range(0, fwidth):
                outFile.write( str( round(flow[y, x, 0], 1) ) + ',' + str( round( flow[y, x, 1], 2) ) + ';' )

        outFile.write('\n')
        prvs = next
        if cv2.waitKey(1) & 0xff == ord('q'):
            break

    else:
        break

print("Done.")
cap.release()
outFile.close()
