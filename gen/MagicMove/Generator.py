import UserInterface
import IOutil
from Definitions import InfoCarrier, MovePattern

ui = UserInterface.UserInterface()
message = ui.gatherEssentialParametersFromUser()
reader = IOutil.ImageInput(message)
image = reader.getImage()
writer = IOutil.VideoOutput(message)

pattern = message.getMovePattern()
direction = message.getMoveDirection()
duration = message.getDuration
if pattern == MovePattern.ZOOM:
    for time in duration*30:
        pass
elif pattern == MovePattern.PAN:
    for time in duration*30:
        pass
elif pattern == MovePattern.Rotate:
    for time in duration*30:
        pass
else:
    print("Abort!")

writer.terminateVideoStream()
