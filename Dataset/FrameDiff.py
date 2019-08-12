import sys
import cv2
from os.path import splitext

inFile = str( sys.argv[1] )
cap = cv2.VideoCapture(inFile)
fps = int( cap.get(cv2.CAP_PROP_FPS) )
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
ret, previous_frame = cap.read()
prvs = cv2.cvtColor(previous_frame, cv2.COLOR_BGR2GRAY)

outFileName = splitext(inFile)[0] + "_diff.mp4"
fourcc = cv2.VideoWriter_fourcc(*'MJPG')
out = cv2.VideoWriter(outFileName, fourcc, fps, (height, width))

while(cap.isOpened()):
    ret, current_frame = cap.read()
    if ret==True:
        print(ret)
        #next = frame2
        curr = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)
        frame_diff = cv2.absdiff(curr, prvs)
        out.write(cv2.cvtColor(frame_diff, cv2.COLOR_GRAY2BGR))
        cv2.imshow('frame2',frame_diff)
        prvs = curr.copy()
        if cv2.waitKey(1) & 0xff == ord('q'):
            break

    else:
        break

cap.release()
out.release()
cv2.destroyAllWindows()
