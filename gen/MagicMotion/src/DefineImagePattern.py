import numpy as np

# 0,0-------------> +x
#  |
#  |
#  |
# \/
# +y

class Triangle:

    def __init__(self, imageBorder):
        halfImageBorder = [imageBorder[0], imageBorder[1], imageBorder[3]]
        self.beforeTransform = np.array( halfImageBorder ).astype(np.float32)
        self.afterTransform = np.array( halfImageBorder ).astype(np.float32)

    def getOriginal(self):
        return self.beforeTransform

    def getShifted(self, x, y):
        for tri in range(0, 3):
            self.afterTransform[tri][0] += x
            self.afterTransform[tri][1] += y
        return self.afterTransform

class Square:

    def __init__(self, imageBorder):
        self.beforeTransform = np.array( imageBorder ).astype(np.float32)
        self.afterTransform = np.array( imageBorder ).astype(np.float32)

    def getOriginal(self):
        return self.beforeTransform

    def getZoomed(self, x, y):
        self.afterTransform[0][0] -= x
        self.afterTransform[0][1] -= y
        self.afterTransform[1][0] += x
        self.afterTransform[1][1] -= y
        self.afterTransform[2][0] += x
        self.afterTransform[2][1] += y
        self.afterTransform[3][0] -= x
        self.afterTransform[3][1] += y
        return self.afterTransform
