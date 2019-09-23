import sys
sys.path.append("src")
import Argument
import IOutils
import ImageProcessing

userCommand = Argument.CommandParser()
userCommand.parseArguments()
inputVideo = userCommand.getInputVideoInfo()
outputVideo = userCommand.getOutputVideoInfo()
outputText = userCommand.getOutputTextInfo()

port = IOutils.IOport(inputVideo, outputVideo, outputText)
port.createFileInstancesUponRequirement()

preprocessor = ImageProcessing.VideoPreprocessor(inputVideo)
preprocessor.findSideToCrop()
preprocessor.findCropPoints()
scaleRatio = preprocessor.getDisplayTargetRatio()

arrowMaker = ImageProcessing.VideoArtist(scaleRatio)
arrowMaker.findBestFrameMapping((8, 8))

monitor = IOutils.Display()

frame = port.getInputVideoFrame()
croppedFrame = preprocessor.cropFrameIntoSquare(frame)
previousFrame = preprocessor.convertFrameIntoSpecifiedFormat(croppedFrame)

while(port.inputVideoIsOpened()):
    try:
        frame = port.getInputVideoFrame()
        croppedFrame = preprocessor.cropFrameIntoSquare(frame)
        currentFrame = preprocessor.convertFrameIntoSpecifiedFormat(croppedFrame)
        OpticalFlow = ImageProcessing.calculateOpticalFlow(previousFrame, currentFrame)
        displayFrame = preprocessor.convertFrameIntoOutputFormat(currentFrame)
        displayFrameMarkedWithFlow = arrowMaker.drawFlowArrows(displayFrame, OpticalFlow)
        port.logDataUponRequirement(displayFrameMarkedWithFlow, OpticalFlow)
        monitor.showFrame(displayFrameMarkedWithFlow)
        previousFrame = currentFrame
    except:
        break
    
port.terminateFileIOUponRequirement()
monitor.terminateAllWindows()

