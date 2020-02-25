import sys

import numpy as np
import cv2

sys.path.append("./")
import Graphics

activity = [4, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0]

gui = Graphics.Graphics()

for i in range(1000):
  gui.displayConfig((3, 3), activity)
  cv2.waitKey(2)
  if i > 500:
    activity = [7, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0]

cv2.destroyAllWindows()
