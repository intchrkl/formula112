class Car(object):
    def __init__(self, x, y, maxspeed):
        self.x = x
        self.y = y
        self.defaultSpeed = maxspeed
        self.offTrackSpeed = maxspeed*1/3
        self.lapCount = 0
        self.sectorsVisited = set()
        self.lapTimes = []

    def getCarCoords(self):
        return (self.x, self.y)

    def getCarSpeed(self, currentSector):
        if currentSector == None:
            return self.offTrackSpeed
        else:
            return self.defaultSpeed
    
    def onFinishLine(self, track, scrollX, scrollY):
        x1, y1, x2, y2 = track.getChecqueredFlag()
        if ((x1-scrollX+track.xshift-(track.width/2) <= self.x <= x2-scrollX+track.xshift+(track.width/2)) and
            (y1-scrollY-track.yshift <= self.y <= y2-scrollY-track.yshift)):
            return True
        return False

        

class PlayerCar(Car):
    def __init__(self, appwidth, appheight, maxspeed):
        super().__init__(appwidth, appheight, maxspeed)

    


    