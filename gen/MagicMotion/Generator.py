import sys
sys.path.append('src')
import UserInterface
import IOutil
import GeometricTransform
from Definitions import InfoCarrier, MovePattern, Zoom, Pan, Rotate

ui = UserInterface.UserInterface()
message = ui.gatherEssentialParametersFromUser()
reader = IOutil.ImageInput(message)
reader.shrinkToFitOutput()
image = reader.getImage()
writer = IOutil.VideoOutput(message)

pattern = message.getMovePattern()
direction = message.getMoveDirection()
duration = message.getDuration()
speed = message.getSpeed()
if pattern == MovePattern.ZOOM:
    proc = GeometricTransform.PerspectiveTransformation(image)
    n = 0
    for time in range(duration*30):
        proc.calculateTransformationMatrix(n, n)
        result = proc.doTransformation()
        writer.writeImageIntoVideo(result)
        if direction == Zoom.IN:
            n += speed
        elif direction == Zoom.OUT:
            n -= speed
elif pattern == MovePattern.PAN:
    proc = GeometricTransform.AffineTransformation(image)
    if direction == Pan.LEFT:
        x, y = -300, 0
    elif direction == Pan.UP:
        x, y = 0, -300
    elif direction == Pan.RIGHT:
        x, y = 300, 0
    elif direction == Pan.DOWN:
        x, y = 0, 300
    for time in range(duration*30):
        proc.calculateTransformationMatrix(x, y)
        result = proc.doTransformation()
        writer.writeImageIntoVideo(result)
        if direction == Pan.LEFT:
            x += speed
        elif direction == Pan.UP:
            y += speed
        elif direction == Pan.RIGHT:
            x -= speed
        elif direction == Pan.DOWN:
            y -= speed
elif pattern == MovePattern.ROTATE:
    proc = GeometricTransform.RotationTransformation(image)
    n = 0
    for time in range(duration*30):
        proc.calculateTransformationMatrix(n, 1.0)
        result = proc.doTransformation()
        writer.writeImageIntoVideo(result)
        if direction == Rotate.CW:
            n += speed
        elif direction == Rotate.CCW:
            n -= speed
else:
    print("Abort!")

writer.terminateVideoStream()
