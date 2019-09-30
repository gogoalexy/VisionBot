import sys
from Definitions import MovePattern, Zoom, Pan, Rotate, InfoCarrier

class UserInterface:

    def __init__(self):
        self.infoPacket = InfoCarrier()
        self.pattern = MovePattern.NA
        
    def unrecognizeable(self):
        print("Unrecognizable option.")
        sys.exit(1)
    
    def collectInputImageName(self):
        inputImageName = input("Enter input image name: ")
        self.infoPacket.setSourceImageName(inputImageName)
    
    def collectOutputVideoName(self):
        outputVideoName = input("Enter output video name: ")
        self.infoPacket.setDestinationVideoName(outputVideoName)
    
    def collectMovePattern(self):
        try:
            pattern = int(input("Enter pattern [Zoom=1/Pan=2/Rotate=3]: "))
            self.pattern = MovePattern(pattern)
            self.infoPacket.setMovePattern(self.pattern)
        except:
            self.infoPacket.setMovePattern(MovePattern.NA)
            self.unrecognizeable()
    
    def collectMoveDirection(self):
        try:
            if self.pattern == MovePattern.ZOOM:
                direction = int(input("Enter direction [in=1/out=2]: "))
                direction = Zoom(direction)
                self.infoPacket.setMoveDirection(direction)
            elif self.pattern == MovePattern.PAN:
                direction = int(input("Enter direction [left=1/up=2/right=3/down=4]: "))
                direction = Pan(direction)
                self.infoPacket.setMoveDirection(direction)
            elif self.pattern == MovePattern.ROTATE:
                direction = int(input("Enter direction [cw=1/ccw=2]: "))
                direction = Rotate(direction)
                self.infoPacket.setMoveDirection(direction)
            else:
                self.unrecognizeable()
        except:
            self.unrecognizeable()
    
    def collectStartPoint(self):
        start = input("Enter the start point x y: ")
        start = tuple(int(e) for e in start.split())
        if len(start) != 2:
            self.unrecognizeable()
        self.infoPacket.setStartPoint(start)
    
    def collectDuration(self):
        try:
            duration = float(input("Enter duration: "))
            self.infoPacket.setDuration(duration)
        except:
            self.unrecognizeable()
    
    def collectSpeed(self):
        speed = input("Enter speed |x| |y|: ")
        speed = tuple(float(e) for e in speed.split())
        if len(speed) != 2:
            self.unrecognizeable()
        self.infoPacket.setSpeed(speed)
    
    def gatherEssentialParametersFromUser(self):
        self.collectInputImageName()
        self.collectOutputVideoName()
        self.collectMovePattern()
        self.collectMoveDirection()
        self.collectStartPoint()
        self.collectDuration()
        self.collectSpeed()
        return self.infoPacket

