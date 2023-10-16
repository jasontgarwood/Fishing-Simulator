#################################################
# mvc.py (gameMode)
#
# Your name: Jason Garwood
# Your andrew id: jgarwood
#################################################
# code animating and playing the game
#################################################################

import random, floater, functions, buttons
from cmu_112_graphics import *
from tkinter import *
from PIL import Image

#################################################################

class gameMode(Mode):
    def appStarted(app):
        # game data initialization
        app.time = 0 
        app.floaters = []
        app.lives = 1
        app.score = 0
        app.onLine = None # the floater that is hooked
        app.isShocking = False # reaction to jellyfish
        app.timeShocked = 0
        app.gameOver = False
        app.isPaused = False
        app.drawInstructions = False
        app.clickMode = False
        app.meterSuccess = False
        app.currMeter = None
        # hook/rod initialization
        app.hMargin = 50
        app.hY = app.width//2
        app.hX = app.width // 2
        app.hasHook = True
        # initialize graphic dimmensions
        app.waterHeight = app.height//4
        app.midWater = app.waterHeight+((app.height-app.waterHeight)//2)
        # initialize spawn rate/ratio/location
        app.fishCaught = 0
        app.spawnEvery = 2800
        app.spawnRatio = ['fish','fish','nothing','trash']
        app.highSpeed = 20
        app.jellyCount,app.sharkCount,app.fastSharkCount = 0,0,0
        app.enemyRate = 3 
        app.minSpawnY = app.waterHeight+30
        app.maxSpawnY = app.height-100
        app.waveTrigger = 200 # amount of points to start next wave/bonus
        # initialize wave 1
        app.currWave = 1
        app.floaters.append(floater.floatingText(app.width,app.height//2,
                            'Catch yellow fish to score points!'))
        functions.createFish(app)

    def keyPressed(app, event):
        if app.gameOver == False and event.key == 'p':
            app.isPaused = not(app.isPaused)
            if app.drawInstructions == True:
                app.drawInstructions = False

    def mousePressed(app,event):
        # control interface when paused
        if app.isPaused == True or app.gameOver == True:
            functions.reactToButtons(app,event)

        else:
            # catch fish and increment score
            if app.onLine != None and event.y < app.waterHeight:
                app.floaters.remove(app.onLine)
                app.score += app.onLine.scoreValue
                app.fishCaught += 1
                app.onLine = None

                # progress game difficulty
                if app.score >= app.waveTrigger: 
                    functions.changeWave(app)

                #increase spawn rate every n fish caught after the first wave
                if app.currWave > 1:
                    app.highSpeed += 1
                    if app.currWave > 2 and app.spawnEvery > 200:
                        app.spawnEvery -= 200
                   
            # reHook line
            if app.hasHook == False and event.y < app.waterHeight:
                app.lives -= 1
                app.hasHook = True
     
    def mouseMoved(app,event):
        if app.gameOver==True or app.isPaused==True or app.currMeter!=None:
            return
        # reel line
        if event.y > app.hMargin:
            app.hY = event.y
        # reel up the fish that is on the line
        for floater in app.floaters:
            if floater.onLine == True:
                floater.x = app.hX
                floater.y = app.hY

    def timerFired(app):          
        if app.isPaused==False and app.gameOver==False and app.currMeter==None:
            app.time += 100
            
            # spawning: create fish,enemies,bonuses, etc.
            if app.time % app.spawnEvery == 0:
                functions.spawnFloater(app)
            
            # move and animate each floater
            for floater in app.floaters:
                # animate through floater image frames
                if floater.__class__.__name__ != 'floatingText':
                    floater.imgIndex = ((floater.imgIndex + 1) % \
                        len(floater.imgList))
                    floater.setImage(floater.imgList[floater.imgIndex],
                                    floater.imageSize)
                # draw animation vertically if hooked on fishing rod
                if floater.onLine == True:
                    if floater.dx > 0:
                        floater.image = floater.image.transpose(
                            Image.ROTATE_90)
                    else:
                        floater.image = floater.image.transpose(
                            Image.ROTATE_270)
                if floater.onLine == False:
                    floater.move(app)

    def redrawAll(app, canvas):
        # draw scenery
        functions.drawSky(app,canvas)
        functions.drawWater(app,canvas)
        functions.drawBoat(app,canvas)

        # draw rod line
        canvas.create_line(app.hX,app.hMargin,app.hX,app.hY)

        # draw hook
        if app.hasHook == True:
            functions.drawHook(app,canvas)
        else:
            canvas.create_text(app.hX+100,app.hMargin,
            text ='Reel up and click to rehook the line!',
            font='Fixedsys 10',fill='gray',anchor=W)
            
        # draw each floater
        for floater in app.floaters:
            floater.draw(canvas)

        # draw jellyfish reaction
        if app.isShocking==True and app.time%200 == 0:
            functions.drawShock(app,canvas)

        # draw score and lives remaining
        functions.drawStats(app,canvas)
        
        # draw waters edge
        canvas.create_rectangle(0,app.waterHeight-10,app.width,
            app.waterHeight,fill='light blue',width=0)
        canvas.create_rectangle(0,app.waterHeight-15,app.width,
            app.waterHeight-10,fill='white',width=0)

        # draw pop-ups
        if app.isPaused == True:
            functions.drawPause(app,canvas,app.width//2,app.height//2)
        if app.gameOver == True:
            functions.drawGameOver(app,canvas,app.width//2,app.height//2)
        if app.gameOver == True or app.isPaused == True:
            if app.drawInstructions == True:
                functions.drawInstructions(app,canvas,app.width//2,
                app.height//2)
   
class clickToCatch(gameMode):
    def appStarted(app):
        super().appStarted()
        app.clickMode = True
        app.aboutToCatch = None
        app.nearHook = False
    
    def mousePressed(app,event):
        super().mousePressed(event)
        if app.currMeter != None and app.aboutToCatch.isClicked(event.x,event.y):
            if app.currMeter.inGreen() == True:
                app.meterSuccess = True
                app.aboutToCatch.reactToHook(app)
            app.currMeter = None
            app.aboutToCatch.speed *= 3
            app.aboutToCatch = None
                     
    def timerFired(app):
        super().timerFired()
        if app.currMeter != None:
            app.currMeter.moveArrow()

    def redrawAll(app,canvas):
        super().redrawAll(canvas)
        if app.currMeter != None:
            app.currMeter.draw(canvas)

class expertMode(clickToCatch):
    def appStarted(app):
        super().appStarted()
        # initialize harder spawn rate/ratio
        app.spawnEvery = 2000
        app.spawnRatio = ['nothing','fish','fish','fish','fish','trash',
                            'shark','shark','fastShark',
                            'jellyfish','jellyfish','fastShark']
        app.highSpeed = 25
        app.waveTrigger = 1000 # amount of points to start next wave/bonus
        app.currWave = 4
        
class homeScreen(Mode):
    def appStarted(app):
        # initialize background animation
        app.backgroundIndex = 0
        app.backgroundFrames=functions.listFiles('images/background')
        app.backgroundImg=Image.open(app.backgroundFrames[app.backgroundIndex])
        app.backgroundImg=app.backgroundImg.resize((app.width,app.height))

        # create buttons 
        app.playButton = buttons.Button(app.width*(1/2),
            app.height*(6/8),100,'PLAY!')
        
        app.normalButton = buttons.Button(app.width*(1/4),
            app.height*(7/16),50,'amateur')
        app.clickToCatchButton = buttons.Button(app.width*(1/2),
            app.height*(7/16),50,'beginner')
        app.expertButton = buttons.Button(app.width*(3/4),
            app.height*(7/16),50,'expert')
        app.helpButton = buttons.Button(app.width*(11/16),app.height*(6/8),30,'?')
        app.helpButton.msgSize = 20
        
        # button toggles
        app.normalButton.isActive = True
        app.clickToCatchButton.isActive = False
        app.expertButton.isActive = False
        app.drawInstructions = False
        
    def timerFired(app):
        # animate background
        app.backgroundIndex=((app.backgroundIndex + 1) % len(
            app.backgroundFrames))
        app.backgroundImg=Image.open(app.backgroundFrames[app.backgroundIndex])
        app.backgroundImg=app.backgroundImg.resize((app.width,app.height))

    def mousePressed(app,event):
        if app.drawInstructions == False:
            # start new game depending on difficulty level
            if app.playButton.isClicked(event.x,event.y) == True:
                if app.clickToCatchButton.isActive == True:
                    app.app.clickToCatchMode = clickToCatch()
                    app.app.setActiveMode(app.app.clickToCatchMode)
                elif app.expertButton.isActive == True:
                    app.app.expertMode = expertMode()
                    app.app.setActiveMode(app.app.expertMode)
                elif app.normalButton.isActive == True:
                    app.app.gameMode = gameMode()
                    app.app.setActiveMode(app.app.gameMode)
                    
            
            # change desired game difficulty based on button selected
            elif app.normalButton.isActive == False and \
                app.normalButton.isClicked(event.x,event.y) == True:
                app.normalButton.isActive = True
                app.clickToCatchButton.isActive = False
                app.expertButton.isActive = False
            elif app.clickToCatchButton.isActive == False and \
                app.clickToCatchButton.isClicked(event.x,event.y) == True:
                app.clickToCatchButton.isActive = True
                app.normalButton.isActive = False
                app.expertButton.isActive = False
            elif app.expertButton.isActive == False and \
                app.expertButton.isClicked(event.x,event.y) == True:
                app.expertButton.isActive = True
                app.clickToCatchButton.isActive = False
                app.normalButton.isActive = False

            elif app.helpButton.isClicked(event.x,event.y) == True:
                app.drawInstructions = True

        # toggle the how-to-play pop-up
        else:
            if app.backButton.isClicked(event.x,event.y) == True:
                app.drawInstructions = False

    def redrawAll(app, canvas):
        # draw background
        canvas.create_image(0,0,anchor=NW,
            image=ImageTk.PhotoImage(app.backgroundImg))

        # draw title
        canvas.create_text(app.width//2,app.height//5,
        text='FISHING SIMULATOR',font='Fixedsys 60',
        fill='dark blue')

        # draw button highlights
        app.normalButton.drawHighlight(canvas)
        app.clickToCatchButton.drawHighlight(canvas)
        app.expertButton.drawHighlight(canvas)

        # draw buttons
        app.playButton.draw(canvas)
        app.normalButton.draw(canvas)
        app.expertButton.draw(canvas)
        app.clickToCatchButton.draw(canvas)
        app.helpButton.draw(canvas)

        # draw popUps
        if app.drawInstructions == True:
            functions.drawInstructions(app,canvas,app.width//2,app.height//2)

class myApp(ModalApp):
    def appStarted(app):
        app._root.resizable(False, False)
        app.homeScreen = homeScreen()
        app.setActiveMode(app.homeScreen)

app = myApp(width=900, height=600)