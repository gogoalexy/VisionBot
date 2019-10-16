from gpiozero import LED

class Indicator():

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
