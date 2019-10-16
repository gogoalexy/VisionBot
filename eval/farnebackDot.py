import sys
import cv2
import time
import numpy as np
import ImageProcessing
import motionFieldTemplate
import snn

NOT_RPi = False

if NOT_RPi:
    pass
else:
    import Indicator

cap = cv2.VideoCapture(0)
if NOT_RPi:
    fps = int( cap.get(cv2.CAP_PROP_FPS) )
    fwidth = int( cap.get(cv2.CAP_PROP_FRAME_WIDTH) )
    fheight = int( cap.get(cv2.CAP_PROP_FRAME_HEIGHT) )
    preprocessor = ImageProcessing.VideoPreprocessor(fheight, fwidth)
    preprocessor.findSideToCrop()
    preprocessor.findCropPoints()
else:
    cap.set(cv2.CAP_PROP_FPS, 32)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 64)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 64)
    preprocessor = ImageProcessing.VideoPreprocessor(64, 64)

ret, frame = cap.read()
if NOT_RPi:
    frame = preprocessor.cropFrameIntoSquare(frame)
prvs = preprocessor.convertFrameIntoSpecifiedFormat(frame)

algo = ImageProcessing.Algorithm()

AllFlattenTemplates = motionFieldTemplate.createAllFlattenTemplate(64, 64)
net = snn.initNet()

while(True):
    start_time = time.time()
    ret, frame = cap.read()
    if ret==True:
        if NOT_RPi:
            frame = preprocessor.cropFrameIntoSquare(frame)
        curr = preprocessor.convertFrameIntoSpecifiedFormat(frame)
        FlattenFlow = algo.calculateOpticalFlow(prvs, curr).flatten()
        dottedFlow = motionFieldTemplate.dotWithTemplates(FlattenFlow, AllFlattenTemplates)
        prvs = curr

    print(dottedFlow)
    snn.run(net, 2000)
    print("FPS: {}".format(1.0 / (time.time() - start_time)))

cap.release()
