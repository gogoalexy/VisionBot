import sys
import cv2
import time
import numpy as np

cap = cv2.VideoCapture(0)
fps = int( cap.get(cv2.CAP_PROP_FPS) )
fwidth = int( cap.get(cv2.CAP_PROP_FRAME_WIDTH) )
fheight = int( cap.get(cv2.CAP_PROP_FRAME_HEIGHT) )
start = time.time()

leftTemplate =
rightTemplate =
forwardTemplate =

ret, frame1 = cap.read()
prvs = cv2.cvtColor(frame1, cv2.COLOR_RGB2GRAY)

while(True):
    ret, frame2 = cap.read()
    if ret==True:
        curr = cv2.cvtColor(frame2, cv2.COLOR_RGB2GRAY)
        flow = cv2.calcOpticalFlowFarneback(prvs, curr, None, 0.5, 3, 15, 3, 5, 1.2, 0)
        forward = np.dot(flow[y, x], forwardP(y, x))
        left = np.dot(flow[y, x], leftP)
        right = np.dot(flow[y, x], rightP)

        prvs = curr
        if cv2.waitKey(1) & 0xff == ord('q'):
            break

end = time.time()
print(end-start)

cap.release()
cv2.destroyAllWindows()
