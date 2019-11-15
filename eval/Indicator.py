
class Indicator():

    def __init__(self):
        try:
            from PiOnly import PiIndicator
            self.show = PiIndicator()
        except:
            self.show = GeneralIndicator()

    def turnOn(self, index):
        self.show.turnOn(index)

    def turnOnConfig(self, threshold, config):
        self.show.turnOnConfig(threshold, config)

    def turnOffAll(self):
        self.show.turnOffAll()

    def turnOff(self, index):
        self.show.turnOff(index)


class GeneralIndicator():

    def __init__(self):
        self.lookup = [ "cw", "ccw", "in", "out", "down", "up", "right", "left",
                        "OBSfront", "OBSrear", "OBSleft", "OBSright" ]

    def turnOn(self, index):
        print(self.lookup[index])

    def turnOnConfig(self, threshold, config):
        for index, activity in enumerate(config, start=0):
            if activity >= threshold:
                print(self.lookup[index])

    def turnOffAll(self):
        pass

    def turnOff(self, index):
        pass

