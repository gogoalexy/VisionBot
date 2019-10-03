import sys
import cv2
import time
import numpy as np
import ImageProcessing
import motionFieldTemplate

cap = cv2.VideoCapture(0)
fps = int( cap.get(cv2.CAP_PROP_FPS) )
fwidth = int( cap.get(cv2.CAP_PROP_FRAME_WIDTH) )
fheight = int( cap.get(cv2.CAP_PROP_FRAME_HEIGHT) )
start = time.time()

preprocessor = ImageProcessing.VideoPreprocessor(fheight, fwidth)
preprocessor.findSideToCrop()
preprocessor.findCropPoints()
algo = ImageProcessing.Algorithm()

leftTemplate = motionFieldTemplate.createCamLeftShiftTemplate(64, 64).flatten()
rightTemplate = motionFieldTemplate.createCamRightShiftTemplate(64, 64).flatten()
upTemplate = motionFieldTemplate.createCamUpShiftTemplate(64, 64).flatten()
downTemplate = motionFieldTemplate.createCamDownShiftTemplate(64, 64).flatten()
forwardTemplate = motionFieldTemplate.createCamZoomInTemplate(64, 64).flatten()
backwardTemplate = motionFieldTemplate.createCamZoomOutTemplate(64, 64).flatten()

ret, frame = cap.read()
croppedFrame = preprocessor.cropFrameIntoSquare(frame)
prvs = preprocessor.convertFrameIntoSpecifiedFormat(croppedFrame)

while(True):
    start_time = time.time()
    ret, frame = cap.read()
    if ret==True:
        croppedFrame = preprocessor.cropFrameIntoSquare(frame)
        curr = preprocessor.convertFrameIntoSpecifiedFormat(croppedFrame)
        flow = algo.calculateOpticalFlow(prvs, curr).flatten()
        forward = np.inner(flow, forwardTemplate)
        backward = np.inner(flow, backwardTemplate)
        left = np.inner(flow, leftTemplate)
        right = np.inner(flow, rightTemplate)
        up = np.inner(flow, upTemplate)
        down = np.inner(flow, downTemplate)

        prvs = curr
        if cv2.waitKey(1) & 0xff == ord('q'):
            break
    print("ZoomIn: {}, ZoomOut: {}, PanLeft: {}, PanRight: {}, PanUp: {}, PanDown: {}".format(forward, backward, left, right, up, down))
    print("FPS: {}".format(1.0 / (time.time() - start_time)))


cap.release()
