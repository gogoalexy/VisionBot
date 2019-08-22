import sys
import cv2
import numpy as np

videoParam = {"size": (256, 256), "time": 20, "fps": 30}
outFileName = str( sys.argv[1] )
fourcc = cv2.VideoWriter_fourcc(*'MJPG')
out = cv2.VideoWriter(outFileName, fourcc, videoParam["fps"], videoParam["size"])

radius = lambda v, t: int(v * t)
circle = {"center": (100, 200), "radius": radius, "thickness": 6, "brigntness": 250, "velocity": 1}
limit = min(videoParam["size"][0]-circle["center"][0], circle["center"][0], videoParam["size"][1]-circle["center"][1], circle["center"][1])

for t in range(0, videoParam["time"]*videoParam["fps"]):
    img = np.zeros(videoParam["size"], dtype=np.uint8)
    r = radius(circle["velocity"], t)
    if r > limit:
        break
    cv2.circle(img, circle["center"], r, color=circle["brigntness"], thickness=circle["thickness"])
    out.write(cv2.cvtColor(img, cv2.COLOR_GRAY2BGR))
    #cv2.imshow("test", img)
    #cv2.waitKey(100)
out.release()
#cv2.destroyAllWindows()
