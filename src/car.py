class Car(object):
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.defaultSpeed = speed
        self.offTrackSpeed = speed*1/3

    def getCarCoords(self):
        return (self.x, self.y)

    def getCarSpeed(self, currentSector):
        if currentSector == None:
            return self.offTrackSpeed
        else:
            return self.defaultSpeed
        

class PlayerCar(Car):
    def __init__(self, appwidth, appheight, speed):
        super().__init__(appwidth, appheight, speed)

    


    