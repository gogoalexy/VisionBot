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
plt.quiver(U, V)

plt.show()
