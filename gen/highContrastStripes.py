import time

import numpy as np
import cv2

height = 2048
width = 2900

image = np.full((height,width,3), 255, np.uint8)
for x in range(0, width, 300):
    image = cv2.line(image, (x, 0), (x+200, 2047), color=(0, 0, 0), thickness=150)

cv2.imwrite("stripes.jpg", image)
time.sleep(1)

cv2.destroyAllWindows()
