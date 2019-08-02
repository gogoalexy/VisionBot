import sys
import cv2
import numpy as np
cap = cv2.VideoCapture(str(sys.argv[1])) # 320*240

BLOCK_W = 16
BLOCK_H = 16

ret, frame1 = cap.read()
prvs = cv2.cvtColor(frame1,cv2.COLOR_BGR2GRAY)
fourcc = cv2.VideoWriter_fourcc(*'MJPG')
out = cv2.VideoWriter('output.avi',fourcc, 20, (320, 240))

while(1):
    ret, frame2 = cap.read()
    if ret==True:
        #next = frame2
        next = cv2.cvtColor(frame2,cv2.COLOR_BGR2GRAY)
        flow = cv2.calcOpticalFlowFarneback(prvs, next, None,0.5, 3, 15, 3, 5, 1.2, 0)

        for y in range(6, 240, BLOCK_H):
            for x in range(6, 320, BLOCK_W):
                cv2.line(frame2, (x, y), (x+int(2*flow[y, x, 0]), y+int(2*flow[y, x, 1])), ( 0, 255, 0 ), thickness=2, lineType=4, shift=0)
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

