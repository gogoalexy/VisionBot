import numpy as np
import time

src = np.arange(0, 8192).reshape(64, 64, 2)
#print(src)

temp = np.arange(8, 8200).reshape(64, 64, 2)
#print(temp)

astart = time.time()
result = 0
for i in range(0, temp.shape[0]):
    for j in range(0, temp.shape[1]):
        product = np.inner(src[i][j], temp[i][j])
        result += product
aend = time.time()
print(result)

bstart = time.time()
result = 0
result = np.inner(src.flatten(), temp.flatten())
bend = time.time()
print(result)

print("-------TIME-------")
print("loop: {}".format(aend - astart))
print("flatten: {}".format(bend - bstart))
