import sys

import matplotlib.pyplot as plt
import numpy as np

sys.path.append("../")
import motionFieldTemplate as mft

def traverseSplitXY(field):
    U = np.empty((field.shape[0], field.shape[1]))
    for y in range(0, field.shape[0]):
        for x in range(0, field.shape[1]):
            U[y][x] = field[y][x][0]
    V = np.empty((field.shape[0], field.shape[1]))
    for y in range(0, field.shape[0]):
        for x in range(0, field.shape[1]):
            V[y][x] = field[y][x][1]
    return U, V

templatex = 16
templatey = 16

plt.figure(0, figsize=(6, 6))
left = mft.createCamLeftShiftTemplate(templatex, templatey)
U, V = traverseSplitXY(left)

plt.subplot(2, 2, 1)
plt.title("Camera Pan Left")
plt.quiver(U, V)


right = mft.createCamRightShiftTemplate(templatex, templatey)
U, V = traverseSplitXY(right)

plt.subplot(2, 2, 2)
plt.title("Camera Pan Right")
plt.quiver(U, V)

# The y axis in OpenCV is quite confusing.
up = mft.createCamUpShiftTemplate(templatex, templatey)
U, V = traverseSplitXY(up)

plt.subplot(2, 2, 3)
plt.title("Camera Pan Up")
plt.quiver(U, V)


down = mft.createCamDownShiftTemplate(templatex, templatey)
U, V = traverseSplitXY(down)

plt.subplot(2, 2, 4)
plt.title("Camera Pan Down")
plt.quiver(U, V)
plt.tight_layout()


plt.figure(1, figsize=(6, 6))
zoomin = mft.createCamZoomInTemplate(templatex, templatey)
U, V = traverseSplitXY(zoomin)

plt.subplot(2, 2, 1)
plt.title("Camera Zoom In")
plt.quiver(U, V)


zoomout = mft.createCamZoomOutTemplate(templatex, templatey)
U, V = traverseSplitXY(zoomout)

plt.subplot(2, 2, 2)
plt.title("Camera Zoom Out")
plt.quiver(U, V)


rotatecw = mft.createCamRotateCWTemplate(templatex, templatey)
U, V = traverseSplitXY(rotatecw)

plt.subplot(2, 2, 3)
plt.title("Camera Rotate CW")
plt.quiver(U, V)


rotateccw = mft.createCamRotateCCWTemplate(templatex, templatey)
U, V = traverseSplitXY(rotateccw)

plt.subplot(2, 2, 4)
plt.title("Camera Rotate CCW")
plt.quiver(U, V)
plt.tight_layout()


plt.figure(2, figsize=(6, 6))
obsrear = mft.createAvoidRearTemplate(templatex, templatey)
U, V = traverseSplitXY(obsrear)

plt.subplot(2, 2, 1)
plt.title("Rear Obstacle")
plt.quiver(U, V)
plt.tight_layout()


obsfront = mft.createAvoidFrontTemplate(templatex, templatey)
U, V = traverseSplitXY(obsfront)

plt.subplot(2, 2, 2)
plt.title("Front Obstacle")
plt.quiver(U, V)
plt.tight_layout()


obsleft = mft.createAvoidLeftTemplate(templatex, templatey)
U, V = traverseSplitXY(obsleft)

plt.subplot(2, 2, 3)
plt.title("Left Obstacle")
plt.quiver(U, V)
plt.tight_layout()


obsright = mft.createAvoidRightTemplate(templatex, templatey)
U, V = traverseSplitXY(obsright)

plt.subplot(2, 2, 4)
plt.title("Right Obstacle")
plt.quiver(U, V)
plt.tight_layout()

plt.show()