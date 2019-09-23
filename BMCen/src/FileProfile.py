class FileProfile:
    
    def __init__(self):
        self.info = {"Name": "", "FPS": 0, "FrameHW": (0, 0), "Active": False, "Instance": None}
    
    def getVideoInfo(self):
        return self.info
    
    def getName(self):
        return self.info["Name"]
    
    def getFPS(self):
        return self.info["FPS"]
    
    def getFrameHeightWidth(self):
        return self.info["FrameHW"]
    
    def getInstance(self):
        return self.info["Instance"]
    
    def setName(self, name: str):
        self.info["Name"] = name
    
    def setFPS(self, fps: int):
        self.info["FPS"] = fps
    
    def setFrameHeightWidth(self, HW):
        self.info["FrameHW"] = HW
    
    def setInstance(self, instance):
        self.info["Instance"] = instance
    
    def activate(self):
        self.info["Active"] = True
    
    def inactivate(self):
        self.info["Active"] = False
    
    def isActivated(self):
        if self.info["Active"]:
            return True
        else:
            return False
    
