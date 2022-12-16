from cmu_112_graphics import *
from car import *
from track import *

import math


def appStarted(app):
    app.currentScreen = "home"

    app.scrollX = 0
    app.scrollY = 0


    #timer
    app.timeElapsed = 0
    app.timerDelay = 10

    trackWidth = 100
    sectorsTrack1 = createtrack1(app) # oval track
    track1 = Track(sectorsTrack1, trackWidth, app, 0)

    sectorsTrack2 = createtrack2(app) # more complex track
    track2 = Track(sectorsTrack2, trackWidth, app, 1)

    sectorsTrack3 = createtrack3(app)
    track3 = Track(sectorsTrack3, trackWidth, app, 2)
    
    app.trackslist = [track1, track2, track3]
    app.track = track1

    # player car
    startFinishStraight = app.track.getSectors()[0]
    xshift = (app.width/2) - (app.track.checkeredFlagX)
    yshift = app.track.getSector(0).y1 - (app.height/2)
    (x1, y1, x2, y2) = startFinishStraight.getSectorCoords()
    maxspeed = 7
    carX = app.track.checkeredFlagX + xshift
    carY = y1 - yshift
    app.playerCar = PlayerCar(carX, carY, maxspeed)
    app.playerCar.currentSector = app.track.sectorsList[0]

    # Loads playercarstrip.png, which stores 24 different orientations of the
    # same car sprite. Then crops the strip into 24 smaller images, and stores 
    # it into a list so that each rotation can be accessed with an index
    # corresponding to a rotation. Based on spritestrip code from: 
    # https://www.cs.cmu.edu/~112/notes/notes-animations-part4.html#spritesheetsWithCropping
    # The image for the car and spritestrip itself was original and drawn by me.
    carspritestrip = app.loadImage('assets/playercarstrip.png')
    app.carsprites = []
    for i in range(24):
        cropx1, cropy1 = (2500/24)*i, 0
        cropx2, cropy2 = (2500/24)*(i+1), 104
        sprite = carspritestrip.crop((cropx1, cropy1, cropx2, cropy2))
        sprite = app.scaleImage(sprite, 2/3)
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

    app.playerLapTimes = []



def createtrack1(app):
    sectors = []
    sector0 = Sector(0, 0, 0, 2000, 0)
    sector1 = Sector(1, 0, 0, 0, 2000)
    sector2 = Sector(2, 0, 2000, 2000, 2000)
    sector3 = Sector(3, 2000, 0, 2000, 2000)
    sectors.append(sector0)
    sectors.append(sector1)
    sectors.append(sector2)
    sectors.append(sector3)
    return sectors

def createtrack2(app):
    sectors = []
    sector0 = Sector(0, 0, 2000, 1500, 2000)
    sector1 = Sector(1, 0, 1000, 0, 2000)
    sector2 = Sector(2, 0, 1000, 1000, 1000)
    sector3 = Sector(3, 1000, 0, 1000, 1000)
    sector4 = Sector(4, 1000, 0, 3000, 0)
    sector5 = Sector(5, 3000, 0, 3000, 1500)
    sector6 = Sector(6, 1500, 1500, 3000, 1500)
    sector7 = Sector(7, 1500, 1500, 1500, 2000)

    sectors.append(sector0)
    sectors.append(sector1)
    sectors.append(sector2)
    sectors.append(sector3)
    sectors.append(sector4)
    sectors.append(sector5)
    sectors.append(sector6)
    sectors.append(sector7)
    return sectors

def createtrack3(app):
    sectors = []
    sector0 = Sector(0, 0, 2000, 2000, 2000)
    sector1 = Sector(1, 0, 0, 0, 2000)
    sector2 = Sector(2, 0, 0, 800, 0)
    sector3 = Sector(3, 800, 0, 800, 1600)
    sector4 = Sector(4, 800, 1600, 1200, 1600)
    sector5 = Sector(5, 1200, 800, 1200, 1600)
    sector6 = Sector(6, 1200, 800, 2000, 800)
    sector7 = Sector(7, 2000, 800, 2000, 2000) 
    sectors.append(sector0)
    sectors.append(sector1)
    sectors.append(sector2)
    sectors.append(sector3)
    sectors.append(sector4)
    sectors.append(sector5)
    sectors.append(sector6)
    sectors.append(sector7)

    return sectors

def updateSectorsVisited(app, car):
    carX, carY = car.getCarCoords()
    currentSector = app.track.getCurrentSectorNum(carX, carY, app.scrollX, app.scrollY)
    car.sectorsVisited.add(currentSector)
    

def updateLapTimes(app):
    currentLapTime = app.timeElapsed - sum(app.playerLapTimes)
    app.playerLapTimes.append(currentLapTime)


def updateLapCount(app, car):
    if None in car.sectorsVisited:
        # removes None from sectorsVisited to ignore when the car goes off-track
        car.sectorsVisited.remove(None)
    if (car.onFinishLine(app.track, app.scrollX, app.scrollY) and 
        len(car.sectorsVisited) == len(app.track.getSectors())):
        # if the car is on the finish line and all the sectors have been visited,
        # update the lap count
        car.lapCount += 1

        # resets the sectorsVisited set for a new lap
        car.sectorsVisited = set()

        # saves the lap time to the timing board
        updateLapTimes(app)

def timerFired(app):
    if app.currentScreen == "game":
        app.timeElapsed += 0.015

    # calls checkTrackLimits, which takes in the car object and will update the
    # app.playerCar.currentSector variable, which keeps track of what sector of the track
    # that the car is currently in.
    checkTrackLimits(app, app.playerCar, app.scrollX, app.scrollY) 
    updateSectorsVisited(app, app.playerCar)
    updateLapCount(app, app.playerCar)

    # if the car is on track, its speed remains unchanged
    # otherwise, decrease the speed of the car if it is off-track
    app.playerCar.updateCarSpeed()

    # moves the track instead of actually moving the car; achieves sidescrolling effect
    app.scrollX -= app.playerCar.vel*math.cos(app.cardirections[app.carOrientation])
    app.scrollY -= app.playerCar.vel*math.sin(app.cardirections[app.carOrientation])
    if app.playerCar.moving:
        # if the car is moving, increase the velocity of the car by 
        # its acceleration value
        app.playerCar.vel = min(app.playerCar.maxvel, app.playerCar.vel+app.playerCar.acc)
    else:
        # otherwise, decelerate the car by its deceleration value
        app.playerCar.vel = max(0, app.playerCar.vel-app.playerCar.decel)
        


def keyPressed(app, event):
    if app.currentScreen == "game":
        if event.key == "Space":
            app.playerCar.moving = bool((int(app.playerCar.moving)+1)%2)
        elif event.key == "Left" or event.key == "a":
            if app.playerCar.vel != 0:
                app.carOrientation -= 1
                if abs(app.carOrientation) > len(app.carsprites)-1:
                    app.carOrientation = app.carOrientation % len(app.carsprites)
        elif event.key == "Right" or event.key == "d":
            if app.playerCar.vel != 0:
                app.carOrientation += 1
                if app.carOrientation > len(app.carsprites)-1:
                    app.carOrientation = app.carOrientation % len(app.carsprites)
        elif event.key == "Escape":
            app.currentScreen = "home"
    elif app.currentScreen == "options":
        pass

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
    elif app.currentScreen == "options":
        x1, y1, x2, y2 = app.width/16, app.height*3/8, app.width*5/16, app.height*5/8
        if x1 <= event.x <= x2 and y1 <= event.y <= y2:
            app.track = app.trackslist[0]
            app.sectorsVisited = set()
        elif (x2+app.width/16 <= event.x <= x2+app.width/16+(x2-x1) and
              y1 <= event.y <= y2):
            app.track = app.trackslist[1]
            app.sectorsVisited = set()
        elif (x2+(2*app.width/16)+(x2-x1) <= event.x <= x2+(2*app.width/16)+2*(x2-x1) and
              y1 <= event.y <= y2):
            app.track = app.trackslist[2]
            app.sectorsVisited = set()
        elif (app.width*6/14 <= event.x <= app.width*8/14 and 
              app.height*7/10 <= event.y <= app.height*8/10):
              app.currentScreen = "home"

def checkTrackLimits(app, car, scrollX, scrollY):
    carX, carY = car.getCarCoords()
    app.playerCar.currentSector = app.track.getCurrentSector(carX, carY, scrollX, scrollY)


def drawCar(app, canvas):
    (x, y) = app.playerCar.getCarCoords()
    canvas.create_image(x, y, 
        image=ImageTk.PhotoImage(app.carsprites[app.carOrientation]))


def drawtrack(app, canvas, track):
    trackWidth = track.getWidth()
    xshift = (app.width/2) - (track.checkeredFlagX)
    yshift = (track.getSector(0).y1) - (app.height/2)
    # draw each sector of the track
    for sector in track.getSectors()[::-1]:
        
        (x1, y1, x2, y2) = sector.getSectorCoords()
        canvas.create_rectangle( x1-trackWidth-app.scrollX+xshift, y1-trackWidth-app.scrollY-yshift,
                        x2+trackWidth-app.scrollX+xshift, y2+trackWidth-app.scrollY-yshift, fill='grey', outline='')

def drawStopwatch(app, canvas):
    minutes = app.timeElapsed // 60
    seconds = app.timeElapsed % 60
    canvas.create_text(app.width/3, app.height*19/20, 
                    text=f"Time Elapsed: {str(round(minutes)).zfill(2)}.{str(round(seconds, 1)).zfill(4)}",
                    fill = 'black', font = 'Arial 24 bold')


def drawGrass(app, canvas):
    canvas.create_rectangle(0,0, app.width, app.height, fill = 'light green')

def drawCurrentSectorText(app, canvas):
    if app.playerCar.currentSector == None:
        sectorText = "Off track!"
        # draws text and warning board
        canvas.create_rectangle(app.width*3/8, app.height*11/15, app.width*5/8, app.height*13/15,
                                fill='bisque2', outline='black', width='5')
        canvas.create_text(app.width/2, app.height*12/15,
                        text="You are off track!", fill = 'maroon',
                        font = 'Arial 36 bold')
    else:
        sectorText = f"Current sector: {app.playerCar.currentSector}"
    
    # displays text of the current sector
    canvas.create_text(app.width/12, app.height*19/20, 
                text=str(sectorText), fill='black', font = 'Arial 24 bold')

def drawLapCounter(app, canvas):
    canvas.create_text(app.width/2, app.height/10, 
                text=f'Laps completed: {app.playerCar.lapCount}', fill='black',
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

def drawMiniMapView(app, canvas, track, x1, y1, x2, y2):
    if track == app.track:
        backgroundcolor = 'light green'
    else:
        backgroundcolor = 'bisque2'
    mapwidth = x2 - x1
    mapheight = y2 - y1
    canvas.create_rectangle(x1, y1, x2, y2, fill=backgroundcolor, outline='black', width=8)
    maxhorizontal = 0
    maxvertical = 0
    minimaptrackwidth = 25
    
    for sector in track.sectorsList:
        xS1, yS1, xS2, yS2 = sector.getSectorCoords()
        vertical = yS2 - yS1
        horizontal = xS2 - xS1
        if horizontal > maxhorizontal:
            maxhorizontal = horizontal
        if vertical > maxvertical:
            maxvertical = vertical


    for sector in track.sectorsList:
        xS1, yS1, xS2, yS2 = sector.getSectorCoords()
        scaledX1 = xS1*mapwidth/(maxhorizontal*2)+(mapwidth/6)
        scaledY1 = yS1*mapheight/(maxvertical*2)+(mapheight/6)
        scaledX2 = xS2*mapwidth/(maxhorizontal*2)+(mapwidth/6)
        scaledY2 = yS2*mapheight/(maxvertical*2)+(mapheight/6)
        canvas.create_line(scaledX1+x1,
                           scaledY1+y1,
                           scaledX2+x1,
                           scaledY2+y1,
                           fill='grey',
                           width=minimaptrackwidth)

    canvas.create_text(x1+(mapwidth/2), y1-(mapheight/5),
                       text=track,
                       fill='maroon',
                       font='Arial 20 bold')

def drawOptionsButtons(app, canvas):
    canvas.create_text(app.width/2, app.height/8, text='Choose your track!',
                       fill='maroon', font='Arial 34 bold')
    canvas.create_text(app.width/2, app.height*7/8,
                        text=f'Currently selected: {app.track}',
                        fill='maroon', font='Arial 34 bold')
    

    canvas.create_rectangle(app.width*6/14, app.height*7/10, app.width*8/14, app.height*8/10,
                            fill='dark grey', outline='black', width=5)
    canvas.create_text(app.width*7/14, app.height*7.5/10,
                            text='Save', fill='black', font='Arial 20 bold')


def drawMiniMapViewWrapper(app, canvas):
    # coordinates of the first minimap frame
    x1, y1, x2, y2 = app.width/16, app.height*3/8, app.width*5/16, app.height*5/8

    # draws each of the tracks in a small frame for the user to view
    drawMiniMapView(app, canvas, app.trackslist[0], x1, y1, x2, y2)
    drawMiniMapView(app, canvas, app.trackslist[1], x2+app.width/16, y1, x2+app.width/16+(x2-x1), y2)
    drawMiniMapView(app, canvas, app.trackslist[2], x2+(2*app.width/16)+(x2-x1), y1, x2+(2*app.width/16)+2*(x2-x1), y2)
                                    
def drawTimingBoard(app, canvas):

    fontsize = 14
    canvas.create_text(app.width/10, app.height/10, 
                           text="Lap times:",
                           font=f"Arial {round(fontsize*3/2)} bold underline",
                           fill='black',
                           anchor='w')

    if app.playerLapTimes != []:
        bestlaptime = min(app.playerLapTimes)
        bestlaptimemin = bestlaptime // 60
        bestlaptimesec = bestlaptime % 60
        bestlaptimetext = f"Best time: {str(round(bestlaptimemin)).zfill(2)}.{str(round(bestlaptimesec, 1)).zfill(4)}"
        canvas.create_text(app.width/10, app.height/10+(fontsize*5/3), 
                            text=bestlaptimetext,
                            font=f"Arial {fontsize} bold",
                            fill='black',
                            anchor='w')

    for i in range(len(app.playerLapTimes)):
        minutes = app.playerLapTimes[i] // 60
        seconds = app.playerLapTimes[i] % 60 
        timeString = f"{str(round(minutes)).zfill(2)}.{str(round(seconds, 1)).zfill(4)}"
        text = f"Lap {i+1}: {timeString}"
        canvas.create_text(app.width/10, app.height/10+((i+2)*(fontsize*5/3)), 
                           text=text,
                           font=f"Arial {fontsize} bold",
                           fill='black',
                           anchor='w')

def drawSpeedometer(app, canvas, car):
    # draws speedometer represented as a progress bar
    currentVel = car.vel
    realisticTopSpeed = 354 # km/h (hypothetical speed)
    realisticVel = currentVel*realisticTopSpeed/car.maxvel
    if realisticVel < 100:
        realisticVelStr = f"  {str(round(realisticVel, 1))}"

    else:
        realisticVelStr = str(round(realisticVel, 1))

    speedometerBarLength = 200

    canvas.create_text(app.width*9.5/15+(speedometerBarLength*5/6), app.height*23.5/25, 
                text=f"{realisticVelStr} km/h", fill='maroon', 
                font = 'Arial 24 bold', anchor='w')

    # progress filler
    canvas.create_rectangle(app.width*9/15, 
                            app.height*23/25, 
                            app.width*9/15+(currentVel/car.maxvel*speedometerBarLength),
                            app.height*24/25,
                            fill='maroon', outline='')

    # outline
    canvas.create_rectangle(app.width*9/15, 
                            app.height*23/25, 
                            app.width*9/15+speedometerBarLength,
                            app.height*24/25,
                            fill='', outline='black', width=2)

def drawTrackLines(app, canvas, track):
    xshift = (app.width/2) - (track.checkeredFlagX)
    yshift = (track.getSector(0).y1) - (app.height/2)

    segmentlength = int(track.width*4/10) # length of each dotted segment in dotted line
    for sector in track.getSectors()[::-1]:
        (x1, y1, x2, y2) = sector.getSectorCoords()
        if sector.orientation == "horizontal":
            for i in range(x1, x2, segmentlength*3):
                canvas.create_line(i-app.scrollX+xshift,
                                   y1-app.scrollY-yshift,
                                   i+segmentlength-app.scrollX+xshift, 
                                   y2-app.scrollY-yshift,
                                   fill='white', width=5)


        elif sector.orientation == "vertical":
            for i in range(y1, y2, segmentlength*3):
                canvas.create_line(x1-app.scrollX+xshift,
                                   i-app.scrollY-yshift,
                                   x2-app.scrollX+xshift, 
                                   i+segmentlength-app.scrollY-yshift,
                                   fill='white', width=5)

def drawCurbs(app, canvas, track):
    xshift = (app.width/2) - (track.checkeredFlagX)
    yshift = (track.getSector(0).y1) - (app.height/2)
    segmentlength = int(track.width*4/10)
    for sector in track.getSectors():
        x1, y1, x2, y2 = sector.getSectorCoords()
        if sector.orientation == "horizontal":
            for i in range(x1-track.width, x2+track.width, segmentlength*2):
                canvas.create_line(i-app.scrollX+xshift,
                                   y1-app.scrollY-yshift-track.width,
                                   i+segmentlength-app.scrollX+xshift, 
                                   y2-app.scrollY-yshift-track.width,
                                   fill='maroon', width=40)
                canvas.create_line(i-app.scrollX+xshift,
                                   y1-app.scrollY-yshift+track.width,
                                   i+segmentlength-app.scrollX+xshift, 
                                   y2-app.scrollY-yshift+track.width,
                                   fill='maroon', width=40)
            for i in range(x1-track.width, x2+track.width-segmentlength, segmentlength*2):
                canvas.create_line(i-app.scrollX+xshift+segmentlength,
                                   y1-app.scrollY-yshift-track.width,
                                   i+(2*segmentlength)-app.scrollX+xshift, 
                                   y2-app.scrollY-yshift-track.width,
                                   fill='white', width=40)
                canvas.create_line(i-app.scrollX+xshift+segmentlength,
                                   y1-app.scrollY-yshift+track.width,
                                   i+(2*segmentlength)-app.scrollX+xshift, 
                                   y2-app.scrollY-yshift+track.width,
                                   fill='white', width=40)
        elif sector.orientation == "vertical":
            for i in range(y1-track.width, y2+track.width, segmentlength*2):
                canvas.create_line(x1-app.scrollX+xshift-track.width,
                                   i-app.scrollY-yshift,
                                   x2-app.scrollX+xshift-track.width, 
                                   i+segmentlength-app.scrollY-yshift,
                                   fill='maroon', width=40)
                canvas.create_line(x1-app.scrollX+xshift+track.width,
                                   i-app.scrollY-yshift,
                                   x2-app.scrollX+xshift+ track.width, 
                                   i+segmentlength-app.scrollY-yshift,
                                   fill='maroon', width=40)
            for i in range(y1-track.width, y2+track.width-segmentlength, segmentlength*2):
                canvas.create_line(x1-app.scrollX+xshift-track.width,
                                   i-app.scrollY-yshift+segmentlength,
                                   x2-app.scrollX+xshift-track.width, 
                                   i+(2*segmentlength)-app.scrollY-yshift,
                                   fill='white', width=40)
                canvas.create_line(x1-app.scrollX+xshift+track.width,
                                   i-app.scrollY-yshift+segmentlength,
                                   x2-app.scrollX+xshift+track.width, 
                                   i+(2*segmentlength)-app.scrollY-yshift,
                                   fill='white', width=40)

def drawFinishLine(app, canvas, track):
    xshift = (app.width/2) - (track.checkeredFlagX)
    yshift = (track.getSector(0).y1) - (app.height/2)
    # draw checkered flag
    (x1, y1, x2, y2) = track.getCheckeredFlag()
    segmentlength = int(track.width*2/10)
    for i in range(y1, y2, segmentlength*2):
                canvas.create_line(x1-app.scrollX+xshift,
                                   i-app.scrollY-yshift,
                                   x2-app.scrollX+xshift, 
                                   i+segmentlength-app.scrollY-yshift,
                                   fill='black', width=segmentlength)
                canvas.create_line(x1-app.scrollX+xshift,
                                   i-app.scrollY-yshift+segmentlength,
                                   x2-app.scrollX+xshift, 
                                   i+(2*segmentlength)-app.scrollY-yshift,
                                   fill='white', width=segmentlength)

                canvas.create_line(x1-app.scrollX+xshift-segmentlength,
                                   i-app.scrollY-yshift,
                                   x2-app.scrollX+xshift-segmentlength, 
                                   i+segmentlength-app.scrollY-yshift,
                                   fill='white', width=segmentlength)
                canvas.create_line(x1-app.scrollX+xshift-segmentlength,
                                   i-app.scrollY-yshift+segmentlength,
                                   x2-app.scrollX+xshift-segmentlength, 
                                   i+(2*segmentlength)-app.scrollY-yshift,
                                   fill='black', width=segmentlength)


    
def redrawAll(app, canvas):
    if app.currentScreen == "home": # home screen
        drawMenuScreen(app, canvas)
    elif app.currentScreen == "options": # menu/options
        drawOptionsButtons(app, canvas)
        drawMiniMapViewWrapper(app, canvas)
    elif app.currentScreen == "game": # start the game
        drawGrass(app, canvas)
        drawCurbs(app, canvas, app.track)
        drawtrack(app, canvas, app.track)
        drawTrackLines(app, canvas, app.track)
        drawFinishLine(app, canvas, app.track)
        drawStopwatch(app, canvas)
        drawTimingBoard(app, canvas)
        drawLapCounter(app, canvas)
        drawCar(app, canvas)
        drawCurrentSectorText(app, canvas)
        drawSpeedometer(app, canvas, app.playerCar)
        
 
def playFormula112():
    appwidth = 1400
    appheight = 800
    apptitle = "Formula 112"
    runApp(width=appwidth,height=appheight, title=apptitle)

def main():
    playFormula112()

if __name__ == '__main__':
    main()