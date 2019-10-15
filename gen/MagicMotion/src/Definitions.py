from enum import Enum
from typing import Tuple

Point2D = Tuple[int, int]

class MovePattern(Enum):
    NA = 0
    ZOOM = 1
    PAN = 2
    ROTATE = 3

class Zoom(Enum):
    NA = 0
    IN = 1
    OUT = 2

class Pan(Enum):
    NA = 0
    LEFT = 1
    UP = 2
    RIGHT = 3
    DOWN = 4

class Rotate(Enum):
    NA = 0
    CW = 1
    CCW = 2

class InfoCarrier:

    def __init__(self):
        self.File = {"SourceImage": "NA", "DestinationVideo": "NA"}
        self.Path = {"MovePattern": MovePattern.NA, "MoveDirection": 0}
        self.Motion = {"StartPoint": (0, 0), "Duration": 5, "Speed": 1.0}

    def setSourceImageName(self, source: str):
        assert isinstance(source, str)
        self.File["SourceImage"] = source

    def setDestinationVideoName(self, destination: str):
        assert isinstance(destination, str)
        self.File["DestinationVideo"] = destination

    def setMovePattern(self, pattern: MovePattern):
        assert isinstance(pattern, MovePattern)
        self.Path["MovePattern"] = pattern

    def setMoveDirection(self, direction: Enum):
        assert isinstance(direction, Enum)
        self.Path["MoveDirection"] = direction

    def setStartPoint(self, point: Point2D):
        assert isinstance(point, tuple)
        self.Motion["StartPoint"] = point

    def setDuration(self, duration: int):
        assert isinstance(duration, int)
        self.Motion["Duration"] = duration

    def setSpeed(self, speed: float):
        assert isinstance(speed, float)
        self.Motion["Speed"] = speed

    def getSourceImageName(self):
        return self.File["SourceImage"]

    def getDestinationVideoName(self):
        return self.File["DestinationVideo"]

    def getMovePattern(self):
        return self.Path["MovePattern"]

    def getMoveDirection(self):
        return self.Path["MoveDirection"]

    def getStartPoint(self):
        return self.Motion["StartPoint"]

    def getDuration(self):
        return self.Motion["Duration"]

    def getSpeed(self):
        return self.Motion["Speed"]

