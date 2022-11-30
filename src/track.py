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
    def __init__(self, sectors, width, app, tracknumber):
        self.sectorsList = sectors # list of sectors
        self.width = width # width of the track
        self.app = app
        self.tracknumber = tracknumber

        # generates the (x1,y1) and (x2,y2) line segment for the start-finish line,
        # which is calculated based on the first sector in the track, and will
        # help with lap counting.
        self.startFinishStraight = self.sectorsList[0]
        (x1, y1, x2, y2) = self.startFinishStraight.getSectorCoords()
        self.checqueredFlagX = (max(x1,x2) - min(x1,x2))/2 + min(x1, x2)
        self.checqueredFlagY1 = y1 - self.width
        self.checqueredFlagY2 = y1 + self.width

        # returns coords of checquered flag in the form (x1, y1, x2, y2)
        self.startFinishLine = self.createStartFinishLine()

        self.xshift = (app.width/2) - (self.checqueredFlagX)
        self.yshift = (self.getSector(0).y1) - (app.height/2)

    def __repr__(self):
        return f"Track {self.tracknumber+1}"

    def createStartFinishLine(self):
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

    def getCurrentSector(self, carX, carY, scrollX, scrollY):
        # returns the sector that the car is currently on, and none if the
        # car is not on any sectors (i.e. the car is off-track)
        for sector in self.sectorsList:
            if sector.orientation == "horizontal":
                xBound1 = sector.x1-self.width-scrollX+self.xshift
                xBound2 = sector.x2+self.width-scrollX+self.xshift
                yBound1 = sector.y1-self.width-scrollY-self.yshift
                yBound2 = sector.y1+self.width-scrollY-self.yshift
                if ((yBound1 <= carY <= yBound2) and
                    (xBound1 <= carX <= xBound2)):
                    return sector
            elif sector.orientation == "vertical":
                xBound1 = sector.x1-self.width-scrollX+self.xshift
                xBound2 = sector.x1+self.width-scrollX+self.xshift
                yBound1 = sector.y1-self.width-scrollY-self.yshift
                yBound2 = sector.y2+self.width-scrollY-self.yshift
                if ((xBound1 <= carX <= xBound2) and
                    (yBound1 <= carY <= yBound2)):
                    return sector
                pass
        return None

    def getCurrentSectorNum(self, carX, carY, scrollX, scrollY):
        sector = self.getCurrentSector(carX, carY, scrollX, scrollY )
        if sector == None:
            return None
        else:
            return sector.sectorNum

    

    