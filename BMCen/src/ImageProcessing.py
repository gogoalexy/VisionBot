import cv2

class VideoPreprocessor:
    
    def __init__(self, videoProfile):
        self.frameHW = videoProfile.getFrameHeightWidth()
        self.cropBegin = 0
        self.cropEnd = 0
        self.cropHorW = ''
        self.targetFrameSize = (64, 64)
        self.displayFrameSize = (512, 512)
    
    def getSideLengthAfterCrop(self):
        return min(self.frameHW)
    
    def getDisplayTargetRatio(self):
        heightRatio = self.displayFrameSize[0]//self.targetFrameSize[0]
        widthRatio = self.displayFrameSize[1]//self.targetFrameSize[1]
        return (heightRatio, widthRatio)
    
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
    
    def convertFrameIntoOutputFormat(self, frame):
        frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
        frame = cv2.resize(frame, self.displayFrameSize, cv2.INTER_LINEAR)
        return frame

class VideoArtist:
    
    def __init__(self, scaleRatio):
        self.defaultLineColor = (3, 173, 255)
        self.defaultLineThickness = 3
        self.defaultLineType = 4
        self.rowMapping = {"start":0, "interval":0, "scale":scaleRatio[0]}
        self.columnMapping = {"start":0, "interval":0, "scale":scaleRatio[1]}
    
    def findBestFrameMapping(self, displayInterval):
        self.rowMapping["interval"] = displayInterval[0]
        self.columnMapping["interval"] = displayInterval[1]
        self.rowMapping["start"] = self.rowMapping["scale"]//2
        self.columnMapping["start"] = self.columnMapping["scale"]//2
    
    def drawFlowArrows(self, frame, flow):
        for y in range(self.rowMapping["start"], flow.shape[0], self.rowMapping["interval"]):
            for x in range(self.columnMapping["start"], flow.shape[1], self.columnMapping["interval"]):
                startPoint = ( x*self.columnMapping["scale"], y*self.rowMapping["scale"] )
                endPoint = ( int(startPoint[0] + flow[y, x, 0]*self.columnMapping["scale"]), int(startPoint[1] + flow[y, x, 1]*self.rowMapping["scale"]) )
                cv2.line(frame, startPoint, endPoint, 
                    color=self.defaultLineColor, thickness=self.defaultLineThickness, lineType=self.defaultLineType)
        return frame

def calculateOpticalFlow(previousFrame, currentFrame):
    flow = cv2.calcOpticalFlowFarneback(previousFrame, currentFrame, None, 0.5, 8, 15, 3, 5, 1.2, 0)
    return flow
    

