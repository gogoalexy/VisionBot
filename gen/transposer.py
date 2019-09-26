import sys
import cv2
from os.path import splitext

inFile = str( sys.argv[1] )
cap = cv2.VideoCapture(inFile)
fps = int( cap.get(cv2.CAP_PROP_FPS) )
HW = tuple([int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)), int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))])
outFileName = splitext(inFile)[0] + "_transpose270.avi"
fourcc = cv2.VideoWriter_fourcc(*'MJPG')
out = cv2.VideoWriter(outFileName, fourcc, fps, (512, 512))

while(cap.isOpened()):
    ret, img = cap.read()
    M = cv2.getRotationMatrix2D((256, 256), 270, 1.0)
    if ret == True:
        rotated90 = cv2.warpAffine(img, M, (512, 512))
        out.write(rotated90)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

cap.release()
out.release()
