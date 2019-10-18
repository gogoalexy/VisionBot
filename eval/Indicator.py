
class Indicator():

    def __init__(self):
        try:
            from PiOnly import PiIndicator
            self.show = PiIndicator()
        except:
            self.show = GeneralIndicator()

    def turnOn(self, index):
        self.show.turnOn(index)

    def turnOffAll(self):
        self.show.turnOffAll()

    def turnOff(self, index):
        self.show.turnOff(index)


class GeneralIndicator():

    def __init__(self):
        self.lookup = [ "upLight", "downLight", "leftLight", "rightLight", "zoominLight", "zoomoutLight", "rotatecwLight", "rotateccwLight" ]

    def turnOn(self, index):
        print(self.lookup[index])

    def turnOffAll(self):
        pass

    def turnOff(self, index):
        print(self.lookup[index])

