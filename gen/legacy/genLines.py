import cv2
import numpy as np

imageSize = (256, 256)

img1 = np.zeros(imageSize, dtype=np.uint8)
cv2.line(img1, (100, 150), (100, 250), 255, thickness=5)
cv2.imwrite('line1.png', img1)

img2 = np.zeros(imageSize, dtype=np.uint8)
cv2.line(img2, (150, 150), (150, 250), 255, thickness=5)
cv2.imwrite('line2.png', img2)
