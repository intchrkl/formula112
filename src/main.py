from cmu_112_graphics import *
from car import *
from track import *

import math


def appStarted(app):
    app.currentScreen = "home"

    app.scrollX = 0
    app.scrollY = 0
    app.scrollXMargin = 500
    app.scrollYMargin = 40


    #timer
    app.timeElapsed = 0

    trackWidth = 50
    sectors = createtrack1(app) # oval track
    # sectors = createtrack2(app) # more complex track
    app.track = Track(sectors, trackWidth, app)
    app.currentSector = sectors[0]
    
    # lap counting system
    app.startFinishLine = app.track.getChecqueredFlag()
    app.lapsCompleted = 0

    # player car
    startFinishStraight = app.track.getSectors()[0]
    xshift = (app.width/2) - (app.track.checqueredFlagX)
    yshift = app.track.getSector(0).y1 - (app.height/2)
    (x1, y1, x2, y2) = startFinishStraight.getSectorCoords()
    carSpeed = 10
    carX = app.track.checqueredFlagX + xshift
    carY = y1 - yshift
    app.playerCar = PlayerCar(carX, carY, carSpeed)

    # loads image of the player's car from assets folder
    # app.carimage = app.loadImage('assets/playercar.png')
    # app.carimage = app.scaleImage(app.carimage, 1/12)

    # Loads playercarstrip.png, which stores 24 different orientations of the
    # same car sprite. Then crops the strip into 24 smaller images, and stores 
    # it into a list so that each rotation can be accessed with an index
    # corresponding to a rotation.
    carspritestrip = app.loadImage('assets/playercarstrip.png')
    app.carsprites = []
    for i in range(24):
        cropx1, cropy1 = (2500/24)*i, 0
        cropx2, cropy2 = (2500/24)*(i+1), 104
        sprite = carspritestrip.crop((cropx1, cropy1, cropx2, cropy2))
        sprite = app.scaleImage(sprite, 1/2)
        app.carsprites.append(sprite)
    
    # creates a list of orientations that the car can face. The number of orientations
    # corresponds to the number of individual sprite orientations, so all the
    # indexes in the carsprites and cardirections list are the same.
    app.cardirections = []
    for i in range(24):
        angle = (i/24)*2*math.pi
        app.cardirections.append(angle)

    # keeps track of the current rotation that the car is facing
    app.carOrientation = 0


def createtrack1(app):
    sectors = []
    sector0 = Sector(0, app.width/5, app.height*4/5, app.width*4/5, app.height*4/5)
    sector1 = Sector(1, app.width/5, app.height/5, app.width/5, app.height*4/5)
    sector2 = Sector(2, app.width/5, app.height/5, app.width*4/5, app.height/5)
    sector3 = Sector(3, app.width*4/5, app.height/5, app.width*4/5, app.height*4/5)
    sectors.append(sector0)
    sectors.append(sector1)
    sectors.append(sector2)
    sectors.append(sector3)
    return sectors

def createtrack2(app):
    sectors = []
    sector0 = Sector(0, app.width/5, app.height*4/5, app.width*3/5, app.height*4/5)
    sector1 = Sector(1, app.width/5, app.height*1/2, app.width/5, app.height*4/5)
    sector2 = Sector(2, app.width/5, app.height*1/2, app.width*2/5, app.height*1/2)
    sector3 = Sector(3, app.width*2/5, app.height/5, app.width*2/5, app.height*1/2)
    sector4 = Sector(4, app.width*2/5, app.height/5, app.width*4/5, app.height/5)
    sector5 = Sector(5, app.width*4/5, app.height/5, app.width*4/5, app.height*3/5)
    sector6 = Sector(6, app.width*3/5, app.height*3/5, app.width*4/5, app.height*3/5)
    sector7 = Sector(7, app.width*3/5, app.height*3/5, app.width*3/5, app.height*4/5)

    sectors.append(sector0)
    sectors.append(sector1)
    sectors.append(sector2)
    sectors.append(sector3)
    sectors.append(sector4)
    sectors.append(sector5)
    sectors.append(sector6)
    sectors.append(sector7)
    return sectors

def createRandomTrack(app):
    sectors = []
    pass

def timerFired(app):
    app.timeElapsed += 0.1 # increments time every 100 milliseconds

    # calls checkTrackLimits, which takes in the car object and will update the
    # app.currentSector variable, which keeps track of what sector of the track
    # that the car is currently in.
    checkTrackLimits(app, app.playerCar, app.scrollX, app.scrollY)

    # checkLaps(app, app.startFinishLine, app.playerCar)


def keyPressed(app, event):
    if app.currentScreen == "game":
        if event.key == "Up" or event.key == "w":
            carSpeed = app.playerCar.getCarSpeed(app.currentSector)
            app.scrollX -= carSpeed*math.cos(app.cardirections[app.carOrientation])
            app.scrollY -= carSpeed*math.sin(app.cardirections[app.carOrientation])
            # makePlayerVisible(app)
            # app.playerCar.x -= carSpeed*math.cos(app.cardirections[app.carOrientation])
            # app.playerCar.y -= carSpeed*math.sin(app.cardirections[app.carOrientation])
        elif event.key == "Down" or event.key == "s":
            carSpeed = app.playerCar.getCarSpeed(app.currentSector)
            app.scrollX += carSpeed*math.cos(app.cardirections[app.carOrientation])
            app.scrollY += carSpeed*math.sin(app.cardirections[app.carOrientation])
            # makePlayerVisible(app)
            # app.playerCar.x += carSpeed*math.cos(app.cardirections[app.carOrientation])
            # app.playerCar.y += carSpeed*math.sin(app.cardirections[app.carOrientation])
        elif event.key == "Left" or event.key == "a":
            app.carOrientation -= 1
            if abs(app.carOrientation) > len(app.carsprites)-1:
                app.carOrientation = app.carOrientation % len(app.carsprites)
        elif event.key == "Right" or event.key == "d":
            app.carOrientation += 1
            if app.carOrientation > len(app.carsprites)-1:
                app.carOrientation = app.carOrientation % len(app.carsprites)

def keyReleased(app, event):
    pass
    
def mousePressed(app, event):
    if app.currentScreen == "home":
        if ((app.width*2/5 <= event.x <= app.width*3/5) and
            (app.height*13/20 <= event.y <= app.height*15/20)):
            app.currentScreen = "options"
        elif ((app.width*2/5 <= event.x <= app.width*3/5) and
            (app.height*4/8 <= event.y <= app.height*5/8)):
            app.currentScreen = "game"


def checkLaps(app, startFinishCoords, car):
    x1, y1, x2, y2 = startFinishCoords
    carX, carY = car.getCarCoords()
    if carX == x1 and y1 <= carY <= y2:
        app.lapsCompleted += 1
        app.playerCar.x -= 1


def checkTrackLimits(app, car, scrollX, scrollY):
    carX, carY = car.getCarCoords()
    app.currentSector = app.track.getCurrentSector(carX, carY, scrollX, scrollY)


def drawCar(app, canvas):
    r = 10
    (x, y) = app.playerCar.getCarCoords()
    # canvas.create_oval(x-r, y-r, x+r, y+r, fill='black')
    # canvas.create_rectangle(x-(2*r), y-r, x+(2*r), y+r, fill='black')
    # canvas.create_image(x, y, image=ImageTk.PhotoImage(app.carimage))
    canvas.create_image(x, y, 
        image=ImageTk.PhotoImage(app.carsprites[app.carOrientation]))


def drawtrack(app, canvas, track):
    trackWidth = track.getWidth()
    xshift = (app.width/2) - (track.checqueredFlagX)
    yshift = (track.getSector(0).y1) - (app.height/2)
    # draw each sector of the track
    for sector in track.getSectors()[::-1]:
        
        (x1, y1, x2, y2) = sector.getSectorCoords()
        if sector.orientation == "horizontal":
            canvas.create_rectangle(x1-trackWidth-app.scrollX+xshift, y1-trackWidth-app.scrollY-yshift,
                        x2+trackWidth-app.scrollX+xshift, y2+trackWidth-app.scrollY-yshift, fill='grey', outline='')

            # outline for each sector
            # canvas.create_rectangle(x1-trackWidth, y1-trackWidth,
            #             x2+trackWidth, y2+trackWidth, fill='', outline='black', width = 2)
        elif sector.orientation == "vertical":
            
            canvas.create_rectangle(x1-trackWidth-app.scrollX+xshift, y1-trackWidth-app.scrollY-yshift,
                        x2+trackWidth-app.scrollX+xshift, y2+trackWidth-app.scrollY-yshift, fill='grey', outline='')

            # outline for each sector                        
            # canvas.create_rectangle(x1-trackWidth, y1-trackWidth,
            #             x2+trackWidth, y2+trackWidth, fill='', outline='black', width = 2)

    # draw checquered flag
    (x1, y1, x2, y2) = track.getChecqueredFlag()
    canvas.create_line(x1-app.scrollX+xshift, y1-app.scrollY-yshift, x2-app.scrollX+xshift, y2-app.scrollY-yshift, fill='white', width='5')

def drawTimingBoard(app, canvas):
    minutes = app.timeElapsed // 60
    seconds = app.timeElapsed % 60 
    canvas.create_text(app.width/3, app.height*19/20, 
                    text=f"Time Elapsed: {round(minutes)}.{round(seconds, 1)}",
                    fill = 'black', font = 'Arial 24 bold')


def drawGrass(app, canvas):
    canvas.create_rectangle(0,0, app.width, app.height, fill = 'light green')

def drawCurrentSectorText(app, canvas):
    if app.currentSector == None:
        sectorText = "Off track!"
        # draws text and warning board
        canvas.create_rectangle(app.width*3/8, app.height*11/15, app.width*5/8, app.height*13/15,
                                fill='bisque2', outline='black', width='5')
        canvas.create_text(app.width/2, app.height*12/15,
                        text="You are off track!", fill = 'maroon',
                        font = 'Arial 36 bold')
    else:
        sectorText = f"Current sector: {app.currentSector}"
    
    # displays text of the current sector
    canvas.create_text(app.width*2/3, app.height*19/20, 
                text=str(sectorText), fill='black', font = 'Arial 24 bold')

def drawLapCounter(app, canvas):
    canvas.create_text(app.width/2, app.height/10, 
                text=f'Laps completed: {app.lapsCompleted}', fill='black',
                font='Arial 24 bold')

def drawMenuScreen(app, canvas):
    # title text
    canvas.create_text(app.width/2, app.height/3,
                        text='Formula 112', fill='maroon', font='Arial 46 bold')

    # start button
    canvas.create_rectangle(app.width*2/5, app.height*10/20, app.width*3/5, app.height*12/20,
                        fill='dark grey', outline='black', width='4')
    canvas.create_text(app.width/2, app.height*11/20, 
                        text='Start', fill='black', font='Arial 24 bold')

    # options button
    canvas.create_rectangle(app.width*2/5, app.height*13/20, app.width*3/5, app.height*15/20,
                        fill='dark grey', outline='black', width='4')
    canvas.create_text(app.width/2, app.height*14/20, 
                        text='Options', fill='black', font='Arial 24 bold')

def drawOptionsScreen(app, canvas):
    pass

def makePlayerVisible(app):
    carX, carY = app.playerCar.getCarCoords()
    # scroll to make player visible as needed
    if (carX < app.scrollX + app.scrollXMargin):
        app.scrollX = carX - app.scrollXMargin
    if (carX > app.scrollX + app.width - app.scrollXMargin):
        app.scrollX = carX - app.width + app.scrollXMargin
    # if (carY < app.scrollY + app.scrollYMargin):
    #     app.scrollY = carY - app.scrollYMargin
    # if (carY > app.scrollY + app.height - app.scrollYMargin):
    #     app.scrollY = carY - app.height + app.scrollYMargin

def drawTrackLimits(app, canvas):
    for sector in app.track.sectorsList:
        if sector.orientation == "horizontal":
            canvas.create_rectangle(sector.x1-app.track.width-app.scrollX+app.track.xshift,
                                    sector.y1-app.track.width-app.scrollY-app.track.yshift,
                                    sector.x2+app.track.width-app.scrollX+app.track.xshift,
                                    sector.y1+app.track.width-app.scrollY-app.track.yshift,
                                    outline='red', width=2)
        elif sector.orientation == "vertical":
            canvas.create_rectangle(sector.x1-app.track.width-app.scrollX+app.track.xshift,
                                    sector.y1-app.track.width-app.scrollY-app.track.yshift,
                                    sector.x1+app.track.width-app.scrollX+app.track.xshift,
                                    sector.y2-app.track.width-app.scrollY-app.track.yshift,
                                    outline='blue', width=2)

def redrawAll(app, canvas):
    if app.currentScreen == "home": # home screen
        drawMenuScreen(app, canvas)
    elif app.currentScreen == "options": # menu/options
        drawOptionsScreen(app, canvas)
    elif app.currentScreen == "game": # start the game
        drawGrass(app, canvas)
        drawtrack(app, canvas, app.track)
        drawTimingBoard(app, canvas)
        drawLapCounter(app, canvas)
        drawCar(app, canvas)
        drawCurrentSectorText(app, canvas)
        
        drawTrackLimits(app, canvas) # temporary

        canvas.create_text(1000, 600, text = f"scrollX: {app.scrollX}", fill='black', font='Arial 14 bold')
        canvas.create_text(1000, 620, text = f"scrollY: {app.scrollY}", fill='black', font='Arial 14 bold')
        canvas.create_text(1000, 700, text = f"carX: {app.playerCar.x}", fill='black', font='Arial 14 bold')
 
def playFormula112():
    appwidth = 1400
    appheight = 800
    apptitle = "Formula 112"
    runApp(width=appwidth,height=appheight, title=apptitle)

def main():
    playFormula112()

if __name__ == '__main__':
    main()