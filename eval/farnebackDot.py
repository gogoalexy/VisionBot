import sys
import cv2
import time
import numpy as np
import motionFieldTemplate

cap = cv2.VideoCapture(0)
fps = int( cap.get(cv2.CAP_PROP_FPS) )
fwidth = int( cap.get(cv2.CAP_PROP_FRAME_WIDTH) )
fheight = int( cap.get(cv2.CAP_PROP_FRAME_HEIGHT) )
start = time.time()

leftTemplate = motionFieldTemplate.createCamLeftShiftTemplate()
rightTemplate = motionFieldTemplate.createCamRightShiftTemplate()
upTemplate = motionFieldTemplate.createCamUpShiftTemplate()
downTemplate = motionFieldTemplate.createCamDownShiftTemplate()
forwardTemplate = motionFieldTemplate.createCamZoomInTemplate()
backwardTemplate = motionFieldTemplate.createCamZoomOutTemplate()

ret, frame1 = cap.read()
prvs = cv2.cvtColor(frame1, cv2.COLOR_RGB2GRAY)

while(True):
    start_time = time.time()
    ret, frame2 = cap.read()
    if ret==True:
        curr = cv2.cvtColor(frame2, cv2.COLOR_RGB2GRAY)
        flow = cv2.calcOpticalFlowFarneback(prvs, curr, None, 0.5, 3, 15, 3, 5, 1.2, 0)
        forward = np.dot(flow, forwardTemplate)
        backward = np.dot(flow, backwardTemplate)
        left = np.dot(flow, leftTemplate)
        right = np.dot(flow, rightTemplate)
        up = np.dot(flow, upTemplate)
        down = np.dot(flow. downTemplate)

        prvs = curr
        if cv2.waitKey(1) & 0xff == ord('q'):
            break
    print("ZoomIn: {}, ZoomOut: {}, PanLeft: {}, PanRight: {}, PanUp: {}, PanDown: {}".format(forward, backward, left, right, up, down))
    print("FPS: {}".format(1.0 / (time.time() - start_time)))


cap.release()
cv2.destroyAllWindows()
