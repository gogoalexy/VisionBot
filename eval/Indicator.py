from gpiozero import LED

class Indicator():

    def __init__():
        upLight = LED(27)
        downLight = LED(22)
        leftLight = LED(4)
        rightLight = LED(17)
        zoominLight = LED(18)
        zoomoutLight = LED(23)
        rotatecwLight = LED(24)
        rotateccwLight = LED(25)
        self.lookup = {"UP": upLight, "DOWN": downLight, "LEFT": leftLight, "RIGHT": rightLight, "ZOOMIN": zoominLight, "ZOOMOUT": zoomoutLight, "ROTATECW": rotatecwLight, "ROTATECCW": rotateccwLight}

    def turnOn(index):
        self.lookup[index].on()

    def turnOff(index):
        self.lookup[index].off()
