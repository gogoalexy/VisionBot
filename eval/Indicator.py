
class Indicator():

    def __init__(self, gpio=False):
        if gpio:
            from gpiozero import LED
            self.show = PiIndicator()
        else:
            self.show = GeneralIndicator()

    def turnOn(self, index):
        self.show.turnOn(index)

    def turnOffAll(self):
        self.show.turnOffAll()

    def turnOff(self, index):
        self.show.turnOff(index)

class PiIndicator():

    def __init__(self):
        upLight = LED(27)
        downLight = LED(22)
        leftLight = LED(4)
        rightLight = LED(17)
        zoominLight = LED(18)
        zoomoutLight = LED(23)
        rotatecwLight = LED(24)
        rotateccwLight = LED(25)
        self.lookup = [ upLight, downLight, leftLight, rightLight, zoominLight, zoomoutLight, rotatecwLight, rotateccwLight ]

    def turnOn(self, index):
        self.lookup[index].on()

    def turnOffAll(self):
        for led in self.lookup:
            led.off()

    def turnOff(self, index):
        self.lookup[index].off()

class GeneralIndicator():

    def __init__(self):
        self.lookup = [ "upLight", "downLight", "leftLight", "rightLight", "zoominLight", "zoomoutLight", "rotatecwLight", "rotateccwLight" ]

    def turnOn(self, index):
        print(self.lookup[index])

    def turnOffAll(self):
        pass

    def turnOff(self, index):
        print(self.lookup[index])

