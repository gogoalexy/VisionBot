import numpy as np

# 0,0-------------> +x
#  |
#  |
#  |
# \/
# +y

class Triangle:

    def __init__(self):
        self.beforeTransform = np.array( [[0, 0], [10, 0], [0, 10]] ).astype(np.float32)
        self.afterTransform = np.array( [[0, 0], [10, 0], [0, 10]] ).astype(np.float32)

    def shift(self, x, y):
        for tri in range(0, 3):
            self.afterTransform[tri][0] += x
            self.afterTransform[tri][1] += y
        return self.afterTransform

    def zoom(self, ratio):
        pass

class Square:
    pass
