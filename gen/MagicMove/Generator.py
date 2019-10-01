import UserInterface
import IOutil
import GeometricTransform
from Definitions import InfoCarrier, MovePattern

ui = UserInterface.UserInterface()
message = ui.gatherEssentialParametersFromUser()
reader = IOutil.ImageInput(message)
reader.shrinkToFitOutput()
image = reader.getImage()
writer = IOutil.VideoOutput(message)

pattern = message.getMovePattern()
direction = message.getMoveDirection()
duration = message.getDuration
if pattern == MovePattern.ZOOM:
    GeometricTransform.PerspectiveTransformation(image)
    for time in duration*30:
        pass
elif pattern == MovePattern.PAN:
    GeometricTransform.AffineTransformation(image)
    for time in duration*30:
        pass
elif pattern == MovePattern.Rotate:
    GeometricTransform.RotationTransformation(image)
    for time in duration*30:
        pass
else:
    print("Abort!")

writer.terminateVideoStream()
