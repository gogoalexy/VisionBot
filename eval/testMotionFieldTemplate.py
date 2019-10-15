import matplotlib.pyplot as plt
import numpy as np
import motionFieldTemplate as mft

left = mft.createCamLeftShiftTemplate(8, 8)
U = np.empty((8, 8))
for y in range(0, 8):
    for x in range(0, 8):
        U[y][x] = left[y][x][0]
V = np.empty((8, 8))
for y in range(0, 8):
    for x in range(0, 8):
        V[y][x] = left[y][x][1]

plt.figure(0)
plt.title("Camera Pan Left")
plt.quiver(U, V)

right = mft.createCamRightShiftTemplate(8, 8)
U = np.empty((8, 8))
for y in range(0, 8):
    for x in range(0, 8):
        U[y][x] = right[y][x][0]
V = np.empty((8, 8))
for y in range(0, 8):
    for x in range(0, 8):
        V[y][x] = right[y][x][1]

plt.figure(1)
plt.title("Camera Pan Right")
plt.quiver(U, V)

up = mft.createCamUpShiftTemplate(8, 8)
U = np.empty((8, 8))
for y in range(0, 8):
    for x in range(0, 8):
        U[y][x] = up[y][x][0]
V = np.empty((8, 8))
for y in range(0, 8):
    for x in range(0, 8):
        V[y][x] = up[y][x][1]

plt.figure(2)
plt.title("Camera Pan Up")
plt.quiver(U, V)

down = mft.createCamDownShiftTemplate(8, 8)
U = np.empty((8, 8))
for y in range(0, 8):
    for x in range(0, 8):
        U[y][x] = down[y][x][0]
V = np.empty((8, 8))
for y in range(0, 8):
    for x in range(0, 8):
        V[y][x] = down[y][x][1]

plt.figure(3)
plt.title("Camera Pan Down")
plt.quiver(U, V)

zoomin = mft.createCamZoomInTemplate(8, 8)
U = np.empty((8, 8))
for y in range(0, 8):
    for x in range(0, 8):
        U[y][x] = zoomin[y][x][0]
V = np.empty((8, 8))
for y in range(0, 8):
    for x in range(0, 8):
        V[y][x] = zoomin[y][x][1]

plt.figure(4)
plt.title("Camera Zoom In")
plt.quiver(U, V)

zoomout = mft.createCamZoomOutTemplate(8, 8)
U = np.empty((8, 8))
for y in range(0, 8):
    for x in range(0, 8):
        U[y][x] = zoomout[y][x][0]
V = np.empty((8, 8))
for y in range(0, 8):
    for x in range(0, 8):
        V[y][x] = zoomout[y][x][1]

plt.figure(5)
plt.title("Camera Zoom Out")
plt.quiver(U, V)

rotatecw = mft.createCamRotateCWTemplate(8, 8)
U = np.empty((8, 8))
for y in range(0, 8):
    for x in range(0, 8):
        U[y][x] = rotatecw[y][x][0]
V = np.empty((8, 8))
for y in range(0, 8):
    for x in range(0, 8):
        V[y][x] = rotatecw[y][x][1]

plt.figure(6)
plt.title("Camera Rotate CW")
plt.quiver(U, V)

rotateccw = mft.createCamRotateCCWTemplate(8, 8)
U = np.empty((8, 8))
for y in range(0, 8):
    for x in range(0, 8):
        U[y][x] = rotateccw[y][x][0]
V = np.empty((8, 8))
for y in range(0, 8):
    for x in range(0, 8):
        V[y][x] = rotateccw[y][x][1]

plt.figure(7)
plt.title("Camera Rotate CCW")
plt.quiver(U, V)

plt.show()
