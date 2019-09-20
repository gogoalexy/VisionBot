import sys
from os.path import splitext
import cv2
import math
import numpy as np
import cProfile
import time

inFile = str( sys.argv[1] )
outFile = open( splitext(inFile)[0] + ".flow", 'w' )
cap = cv2.VideoCapture(inFile)
fps = int( cap.get(cv2.CAP_PROP_FPS) )
fwidth = int( cap.get(cv2.CAP_PROP_FRAME_WIDTH) )
fheight = int( cap.get(cv2.CAP_PROP_FRAME_HEIGHT) )
vlength = int( cap.get(cv2.CAP_PROP_FRAME_COUNT) )
center = tuple([fwidth/2.0, fheight/2.0])

def forwardP(y, x):
    i = x - center[0]
    j = y - center[1]
    norm = math.sqrt(i**2 + j**2)
    if norm:
        return tuple([i/norm, j/norm])
    else:
        return tuple([0, 0])

leftP = tuple([1, 0])
rightP = tuple([-1, 0])

print("Input file: {} fps, {} frames, {} pixels wide, {} pixels high".format(fps, vlength,fwidth, fheight))
print("Processing...")

ret, frame1 = cap.read()
prvs = cv2.cvtColor(frame1, cv2.COLOR_RGB2GRAY)

resultF = []
resultL = []
resultR = []

start = time.time()

while(1):
    vlength = vlength - 1
    ret, frame2 = cap.read()
    if ret==True:
        curr = cv2.cvtColor(frame2, cv2.COLOR_RGB2GRAY)
        flow = cv2.calcOpticalFlowFarneback(prvs, curr, None, 0.5, 3, 15, 3, 5, 1.2, 0)
        print("{} frames remain".format(vlength))
        forward = 0.0
        left = 0.0
        right = 0.0
        outFile.write('[')
        for y in range(0, fheight):
            for x in range(0, fwidth):
            #    if x == fwidth - 1:
            #        outFile.write( str( (flow[y, x, 0]) ) + ',' + str( ( flow[y, x, 1]) ) )
            #    else:
            #        outFile.write( str( (flow[y, x, 0]) ) + ',' + str( ( flow[y, x, 1]) ) + ',' )
            # outFile.write(';')
                forward += np.dot(flow[y, x], forwardP(y, x))
                left += np.dot(flow[y, x], leftP)
                right += np.dot(flow[y, x], rightP)

        outFile.write(']\n')
        resultF.append(forward)
        resultL.append(left)
        resultR.append(right)
        # print( "{}, {}, {}".format(str(forward), str(left), str(right)) )
        prvs = curr
        if cv2.waitKey(1) & 0xff == ord('q'):
            break

    else:
        outFile.write("forward:")
        s = ''.join(str(resultF))
        outFile.write(s)
        outFile.write('\n')
        outFile.write("left:")
        s = ''.join(str(resultL))
        outFile.write(s)
        outFile.write('\n')
        outFile.write("right:")
        s = ''.join(str(resultR))
        outFile.write(s)
        outFile.write('\n')
        break
end = time.time()
print("Done.")
print(end-start)
cap.release()
outFile.close()
