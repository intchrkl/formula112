class Car(object):
    def __init__(self, x, y, maxvel):
        self.x = x
        self.y = y
        self.vel = 0
        self.acc = 0.1
        self.decel = 0.05
        self.maxvel = maxvel
        self.offTrackVel = maxvel*1/3
        self.currentSector = 0
        self.lapCount = 0
        self.sectorsVisited = set()
        self.lapTimes = []
        self.moving = False

    def getCarCoords(self):
        return (self.x, self.y)

    def updateCarSpeed(self):
        if self.currentSector == None:
            self.vel = self.vel*19/20
    
    def onFinishLine(self, track, scrollX, scrollY):
        x1, y1, x2, y2 = track.getChecqueredFlag()
        if ((x1-scrollX+track.xshift-(track.width/2) <= self.x <= x2-scrollX+track.xshift+(track.width/2)) and
            (y1-scrollY-track.yshift <= self.y <= y2-scrollY-track.yshift)):
            return True
        return False

        

class PlayerCar(Car):
    def __init__(self, appwidth, appheight, maxvel):
        super().__init__(appwidth, appheight, maxvel)

    


    