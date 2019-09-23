import cv2
from os.path import splitext
import FileProfile

class IOport:
    
    def __init__(self, inputVideoProfile, outputVideoProfile, outputTextProfile):
        self.inputVideo = inputVideoProfile
        self.outputVideo = outputVideoProfile
        self.outputText = outputTextProfile
        self.defaultOutputVideoName = splitext(self.inputVideo.getName())[0] + "_FB.avi"
        self.defaultOutputVideoFrameHW = (512, 512)
        self.defaultOutputVideoFourcc = cv2.VideoWriter_fourcc(*'MJPG')
        self.defaultOutputTextFileName = splitext(self.inputVideo.getName())[0] + ".flow"
    
    def createInputVideoInstance(self):
        try:
            inputVideoInstance = cv2.VideoCapture(self.inputVideo.getName())
            self.inputVideo.setInstance(inputVideoInstance)
        except:
            inputVideoInstance = cv2.VideoCapture(0)
            self.inputVideo.setInstance(inputVideoInstance)
        finally:
            fps = int( self.inputVideo.getInstance().get(cv2.CAP_PROP_FPS) )
            frameWidth = int( self.inputVideo.getInstance().get(cv2.CAP_PROP_FRAME_WIDTH) )
            frameHeight = int( self.inputVideo.getInstance().get(cv2.CAP_PROP_FRAME_HEIGHT) )
            self.inputVideo.setFPS(fps)
            self.inputVideo.setFrameHeightWidth( (frameHeight, frameWidth) )
    
    def createOutputVideoInstance(self):
        outputVideoInstance = cv2.VideoWriter(self.defaultOutputVideoName, 
            self.defaultOutputVideoFourcc, self.inputVideo.getFPS(), self.defaultOutputVideoFrameHW)
        self.outputVideo.setName(self.defaultOutputVideoName)
        self.outputVideo.setFPS(self.inputVideo.getFPS())
        self.outputVideo.setFrameHeightWidth(self.defaultOutputVideoFrameHW)
        self.outputVideo.setInstance(outputVideoInstance)
    
    def createOutputTextFileInstance(self):
        outputTextFileInstance = open(self.defaultOutputTextFileName, 'w')
        self.outputText.setName(self.defaultOutputTextFileName)
        self.outputText.setInstance(outputTextFileInstance)
    
    def createFileInstancesUponRequirement(self):
        if self.inputVideo.isActivated():
            self.createInputVideoInstance()
        if self.outputVideo.isActivated():
            self.createOutputVideoInstance()
        if self.outputText.isActivated():
            self.createOutputTextFileInstance()
    
    def terminateInputVideoIO(self):
        self.inputVideo.getInstance().release()
    
    def terminateOutputVideoIO(self):
        self.outputVideo.getInstance().release()
    
    def terminateTextIO(self):
        self.outputText.getInstance().close()
    
    def terminateFileIOUponRequirement(self):
        if self.inputVideo.isActivated():
            self.terminateInputVideoIO()
        if self.outputVideo.isActivated():
            self.terminateOutputVideoIO()
        if self.outputText.isActivated():
            self.terminateTextIO()
    
    def inputVideoIsOpened(self):
        state = ( self.inputVideo.getInstance() ).isOpened()
        return state
    
    def outputVideoIsOpened(self):
        state = ( self.outputVideo.getInstance() ).isOpened()
        return state
    
    def getInputVideoFrame(self):
        ret, frame = self.inputVideo.getInstance().read()
        if ret:
            return frame
        else:
            raise Exception
    
    def writeFrame(self, frame):
        self.outputVideo.getInstance().write(frame)
    
    def writeFlow(self, flow):
        self.outputText.getInstance().write('[')
        for y in range(0, flow.shape[0]):
            for x in range(0, flow.shape[1]):
                if x == flow.shape[1] - 1:
                    self.outputText.getInstance().write( str( round(flow[y, x, 0], 2) ) + ',' + str( round( flow[y, x, 1], 2) ) )
                else:
                    self.outputText.getInstance().write( str( round(flow[y, x, 0], 2) ) + ',' + str( round( flow[y, x, 1], 2) ) + ',' )
            self.outputText.getInstance().write(';')
        self.outputText.getInstance().write(']\n')
    
    def logDataUponRequirement(self, frame, flow):
        if self.outputVideo.isActivated():
            self.writeFrame(frame)
        if self.outputText.isActivated():
            self.writeFlow(flow)
    
class Display:
    
    def __init__(self):
        self.defaultNameOfWindow = "Optical Flow"
    
    def showFrame(self, frame):
        cv2.imshow(self.defaultNameOfWindow, frame)
        cv2.waitKey(1)
    
    def terminateAllWindows(self):
        cv2.destroyAllWindows()
    

