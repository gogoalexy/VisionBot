import cv2
import numpy as np

src = cv2.imread("target.jpg")
outFileName = "move.avi"
fourcc = cv2.VideoWriter_fourcc(*'MJPG')
out = cv2.VideoWriter(outFileName, fourcc, 30, (512, 512))

srcTri = np.array( [[0, 0], [1000, 0], [0, 1000]] ).astype(np.float32)
dstTri = np.array( [[100, 0], [1100, 0], [100, 1000]] ).astype(np.float32)
warp_mat = cv2.getAffineTransform(srcTri, dstTri)
warp_dst = cv2.warpAffine(src, warp_mat, (src.shape[1], src.shape[0]), borderValue=(0, 255, 255))

cv2.imshow("", warp_dst)
cv2.waitKey(0)

cv2.destroyAllWindows()
