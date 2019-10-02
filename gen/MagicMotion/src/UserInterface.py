import sys
from os.path import splitext
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
        rawOutputVideoName = input("Enter output video name: ")
        outputVideoName = splitext(rawOutputVideoName)[0] + '.avi'
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
            duration = int(input("Enter duration (seconds): "))
            self.infoPacket.setDuration(duration)
        except:
            self.unrecognizeable()

    def collectSpeed(self):
        try:
            speed = float(input("Enter speed |v|: "))
            self.infoPacket.setSpeed(speed)
        except:
            self.unrecognizeable()

    def gatherEssentialParametersFromUser(self):
        self.collectInputImageName()
        self.collectOutputVideoName()
        self.collectMovePattern()
        self.collectMoveDirection()
        # self.collectStartPoint()
        self.collectDuration()
        self.collectSpeed()
        return self.infoPacket

