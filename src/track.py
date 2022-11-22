class Sector(object):
    # A Sector object represents the different straight sections on a track,
    # similarly to how a racetrack in real life would have multiple sections.
    # A section is created by dedicating it a number, and its start and end
    # point (x1,y1), (x2,y2), since we are representing a sector as a line segment.
    def __init__(self, sectorNumber, x1, y1, x2, y2):
        self.x1, self.y1 = x1, y1
        self.x2, self.y2 = x2, y2
        self.sectorNum = sectorNumber
        if x1 == x2:
            self.orientation = "vertical"
        elif y1 == y2:
            self.orientation = "horizontal"

    def __repr__(self):
        return str(self.sectorNum)

    def getSectorCoords(self):
        return (self.x1, self.y1, self.x2, self.y2)

class Track(object):
    # A Track object consists of a list of sectors, which, put together will
    # create a unique track. This allows tracks to be 'modular', since sectors
    # can be added and removed. This will hopefully allow for random track
    # generation to be added in later stages.
    def __init__(self, sectors, width):
        self.sectorsList = sectors # list of sectors
        self.width = width # width of the track

        # returns coords of checquered flag in the form (x1, y1, x2, y2)
        self.startFinishLine = self.createStartFinishLine()

    def createStartFinishLine(self):
        # generates the (x1,y1) and (x2,y2) line segment for the start-finish line,
        # which is calculated based on the first sector in the track, and will
        # help with lap counting.
        startFinishStraight = self.sectorsList[0]
        (x1, y1, x2, y2) = startFinishStraight.getSectorCoords()
        self.checqueredFlagX = (max(x1,x2) - min(x1,x2))/2 + min(x1, x2)
        self.checqueredFlagY1 = y1 - self.width
        self.checqueredFlagY2 = y1 + self.width
        return (self.checqueredFlagX, self.checqueredFlagY1, 
                self.checqueredFlagX, self.checqueredFlagY2)

    def getSectors(self):
        return self.sectorsList

    def getChecqueredFlag(self):
        return self.startFinishLine

    def getNumSectors(self):
        return len(self.sectorsList)

    def getWidth(self):
        return self.width

    def getSector(self, sectorNum):
        return self.sectorsList[sectorNum]

    def getCurrentSector(self, carX, carY):
        # returns the sector that the car is currently on, and none if the
        # car is not on any sectors (i.e. the car is off-track)
        for sector in self.sectorsList:
            if sector.orientation == "horizontal":
                if ((sector.y1-self.width <= carY <= sector.y1+self.width) and
                        sector.x1-self.width <= carX <= sector.x2+self.width):
                    return sector
            elif sector.orientation == "vertical":
                if ((sector.x1-self.width <= carX <= sector.x1+self.width) and
                        sector.y1-self.width <= carY <= sector.y2+self.width):
                    return sector
        return None

    