import sys
import cv2
import numpy as np

def cropBorder(srcLength, dstLength):
    center = srcLength//2
    half = divmod(dstLength, 2)
    begin = center - half[0]
    end = center + half[0]
    if half[1]:
        end += 1

    return begin, end

def isOut(radius, thickness, limit):
    graphBorder = radius + thickness/2
    if graphBorder > limit or graphBorder < 0:
        return True
    else:
        return False

videoParam = {"size": (1024, 1024), "outSize": (512, 512),"time": 5, "fps": 30}
outFileName = str( sys.argv[1] )
fourcc = cv2.VideoWriter_fourcc(*'MJPG')
out = cv2.VideoWriter(outFileName, fourcc, videoParam["fps"], videoParam["outSize"])
verticalCropPoint = cropBorder(videoParam["size"][0], videoParam["outSize"][0])
horizontalCropPoint = cropBorder(videoParam["size"][1], videoParam["outSize"][1])

marker = {"type": cv2.MARKER_SQUARE, "position": (512, 512), "initialSize": 100, "initialThickness": 5, "brigntness": 250, "velocity": 4}
shortestLenhth2border = min(videoParam["size"][0]-marker["position"][0], marker["position"][0], videoParam["size"][1]-marker["position"][1], marker["position"][1])

angle = 0

for t in range(0, videoParam["time"]*videoParam["fps"]):
    img = np.zeros(videoParam["size"], dtype=np.uint8)
    if t == 0:
        size = marker["initialSize"]
        thic = marker["initialThickness"]
    else:
        angle += marker["velocity"]
        rotate = cv2.getRotationMatrix2D((512, 512), angle, 1.0) 

    if isOut(size, thic, shortestLenhth2border):
        print("Warning: Graph is out of border. Interrupted.")
        break
    
    cv2.drawMarker(img, marker["position"], marker["brigntness"], marker["type"], int(size), int(thic))
    if t != 0:
        img = cv2.warpAffine(img, rotate, (videoParam["size"]))
    outImg = img[verticalCropPoint[0]:verticalCropPoint[1], horizontalCropPoint[0]:horizontalCropPoint[1]]
    out.write(cv2.cvtColor(outImg, cv2.COLOR_GRAY2BGR))
    cv2.imshow("test", outImg)
    cv2.waitKey(100)
out.release()
cv2.destroyAllWindows()
