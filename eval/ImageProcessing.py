import cv2

class VideoPreprocessor:

    def __init__(self, videoHeight, videoWidth):
        self.frameHW = (videoHeight, videoWidth)
        self.cropBegin = 0
        self.cropEnd = 0
        self.cropHorW = ''
        self.targetFrameSize = (64, 64)

    def getSideLengthAfterCrop(self):
        return min(self.frameHW)

    def sortSideLength(self):
        longer = max(self.frameHW)
        shorter = min(self.frameHW)
        return longer, shorter

    def findSideToCrop(self):
        if self.frameHW[0] > self.frameHW[1]:
            self.cropHorW = 'H'
        elif self.frameHW[0] < self.frameHW[1]:
            self.cropHorW = 'W'
        else:
            self.cropHorW = 'N'

    def findCropPoints(self):
        longerSide, shorterSide = self.sortSideLength()
        cropCenter = longerSide//2
        halfLength = divmod(shorterSide, 2)
        self.cropBegin = cropCenter - halfLength[0]
        self.cropEnd = cropCenter + halfLength[0]
        if halfLength[1]:
            self.cropEnd += 1

    def cropFrameIntoSquare(self, frame):
        if self.cropHorW == 'H':
            croppedFrame = frame[self.cropBegin:self.cropEnd, 0:]
            return croppedFrame
        elif self.cropHorW == 'W':
            croppedFrame = frame[0:, self.cropBegin:self.cropEnd]
            return croppedFrame
        else:
            return frame

    def convertFrameIntoSpecifiedFormat(self, frame):
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame = cv2.resize(frame, self.targetFrameSize, cv2.INTER_AREA)
        return frame


class Algorithm:

    def calculateOpticalFlow(self, previousFrame, currentFrame):
        flow = cv2.calcOpticalFlowFarneback(previousFrame, currentFrame, None, 0.5, 8, 15, 3, 5, 1.2, 0)
        return flow

    def contrastEnhance(self, frame):
        # GaussianKernalSize1 = 7
        # GaussianSTD1 = 5.0
        blur = cv2.GaussianBlur(frame, (7, 7), 5.0)
        unsharpFrame = cv2.addWeighted(frame, t, blur, -4, 0, frame)
        return unsharpFrame

