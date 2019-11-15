import sys

import numpy as np
import matplotlib.pyplot as plt

xfile = open("../assets/matricesX.txt", 'r')
yfile = open("../assets/matricesY.txt", 'r')

xFields = [[], [], [], [], [], [], [], []]
yFields = [[], [], [], [], [], [], [], []]
for line in xfile:
    motions = line.split()
    for container, element in zip(xFields, motions):
        container.append(float(element))

for line in yfile:
    motions = line.split()
    for container, element in zip(yFields, motions):
        container.append(float(element))


plt.figure(0, figsize=(6, 6))

U = np.array(xFields[0]).reshape((64, 64))
V = np.array(yFields[0]).reshape((64, 64))
plt.subplot(2, 2, 1)
plt.title("Camera Rotate CCW")
plt.quiver(U, V)


U = np.array(xFields[1]).reshape((64, 64))
V = np.array(yFields[1]).reshape((64, 64))
plt.subplot(2, 2, 2)
plt.title("Camera Zoom In")
plt.quiver(U, V)


U = np.array(xFields[2]).reshape((64, 64))
V = np.array(yFields[2]).reshape((64, 64))
plt.subplot(2, 2, 3)
plt.title("Camera Pan Down")
plt.quiver(U, V)


U = np.array(xFields[3]).reshape((64, 64))
V = np.array(yFields[3]).reshape((64, 64))
plt.subplot(2, 2, 4)
plt.title("Camera Pan Right")
plt.quiver(U, V)
plt.tight_layout()

plt.figure(1, figsize=(6, 6))

U = np.array(xFields[4]).reshape((64, 64))
V = np.array(yFields[4]).reshape((64, 64))
plt.subplot(2, 2, 1)
plt.title("Front obstacle")
plt.quiver(U, V)


U = np.array(xFields[5]).reshape((64, 64))
V = np.array(yFields[5]).reshape((64, 64))
plt.subplot(2, 2, 2)
plt.title("Rear obstacle")
plt.quiver(U, V)


U = np.array(xFields[6]).reshape((64, 64))
V = np.array(yFields[6]).reshape((64, 64))
plt.subplot(2, 2, 3)
plt.title("Left obstacle")
plt.quiver(U, V)


U = np.array(xFields[7]).reshape((64, 64))
V = np.array(yFields[7]).reshape((64, 64))
plt.subplot(2, 2, 4)
plt.title("Right obstacle")
plt.quiver(U, V)
plt.tight_layout()

plt.show()
