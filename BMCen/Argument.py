import argparse
import FileProfile

class CommandParser:
    
    def __init__(self):
        self.argumentParser = argparse.ArgumentParser(prog="calcOpticalFlow",
            description="A mini program for calculating optical flow with different algorithms.")
        self.videoSource = self.argumentParser.add_mutually_exclusive_group(required=True)
        self.videoSource.add_argument("-i", "--input", type=str, help="input video name")
        self.videoSource.add_argument("-s", "--stream", action="store_true", help="switch to video stream input")
        self.argumentParser.add_argument("-o", "--outputvideo", action="store_true", help="output processed video")
        self.argumentParser.add_argument("-flow", "--outputflow", action="store_true", help="output .flow file")
    
    def parseArguments(self):
            self.argumentResults = self.argumentParser.parse_args()
    
    def getInputVideoInfo(self):
        self.inputVideo = FileProfile.FileProfile()
        if self.argumentResults.input:
            self.inputVideo.activate()
            self.inputVideo.setName(self.argumentResults.input)
        elif self.argumentResults.stream:
            self.inputVideo.inactivate()
            self.inputVideo.setName("stream.mjpg")
        return self.inputVideo
    
    def getOutputVideoInfo(self):
        self.outputVideo = FileProfile.FileProfile()
        if self.argumentResults.outputvideo:
            self.outputVideo.activate()
            self.outputVideo.setName(self.argumentResults.outputvideo)
        return self.outputVideo
    
    def getOutputTextInfo(self):
        self.outputText = FileProfile.FileProfile()
        if self.argumentResults.outputflow:
            self.outputText.activate()
            self.outputText.setName(self.argumentResults.outputflow)
        return self.outputText
    

