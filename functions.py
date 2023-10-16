#################################################
# TP.functions.py
#
# Your name: Jason Garwood
# Your andrew id: jgarwood
#################################################
# code with helper functions and functions used in more than one instance
#################################################################

import math, random, floater, os, buttons
from cmu_112_graphics import *
from tkinter import *
from PIL import Image

#################################################################

# returns the distance between two points
def distance(x0,y0,x1,y1):
   return math.sqrt(((x0-x1)**2)+((y0-y1)**2))

######### make floater objects

# returns parameters for a floater object
def floaterParams(app):
    x = random.choice([0,app.width])
    y = random.randint(app.minSpawnY,app.maxSpawnY)
    if x == 0:
        dx = 1
    else:
        dx = -1
    speed = random.randint(5,app.highSpeed)
    return x,y,dx,speed

# creates a random floater based on ratio defined in app
def spawnFloater(app):
    spawnType = random.choice(app.spawnRatio)
    if spawnType == 'fish':
        createFish(app)
    elif spawnType == 'bigFish':
        createBigFish(app)
    elif spawnType == 'biggerFish':
        createBiggerFish(app)
    elif spawnType == 'trash':
        createTrash(app)
    elif spawnType == 'shark':
        createShark(app)
    elif spawnType == 'jellyfish':
        createJellyfish(app)
    elif spawnType == 'fastShark':
        createFastShark(app)

### make fish objects

def createFish(app):
    x,y,dx,speed = floaterParams(app)
    app.floaters.append(floater.Fish(x,y,dx,speed))

def createBigFish(app):
    x,y,dx,speed = floaterParams(app)
    app.floaters.append(floater.bigFish(x,y,dx,speed))

def createBiggerFish(app):
    x,y,dx,speed = floaterParams(app)
    app.floaters.append(floater.biggerFish(x,y,dx,speed))
    
### make enemy objects

def createTrash(app):
    x,y,dx,speed = floaterParams(app)
    app.floaters.append(floater.Trash(x,y,dx,speed))

def createShark(app):
    x,y,dx,speed = floaterParams(app)
    app.floaters.append(floater.Shark(x,y,dx,speed))

def createJellyfish(app):
    x,y,dx,speed = floaterParams(app)
    app.floaters.append(floater.Jellyfish(x,y,dx,speed))

def createFastShark(app):
    x,y,dx,speed = floaterParams(app)
    app.floaters.append(floater.FastShark(x,y,dx,speed))

### make bonus objects

def createExtraHook(app):
    x,y,dx,speed = floaterParams(app)
    app.floaters.append(floater.extraHook(x,y,dx,speed))
    if dx > 0:
        app.floaters.append(floater.Jellyfish(x+60,y-40,dx,speed))
    else:
        app.floaters.append(floater.Jellyfish(x-60,y-40,dx,speed))

######### increase game difficulty

# changes the spawn-rate ratio of floater object's types and advances currWave 
def changeWave(app):
    app.waveTrigger *= 3
    if app.currWave < 4:
        app.currWave += 1
        # create message floaters and introduce new object types
        if app.currWave == 2:
            msg = 'Catch bigger fish with smaller ones as bait!'
            app.floaters.append(floater.floatingText(app.width,app.height//2+50,
            '                      Sharks can break your hook!!'))
            createBigFish(app)
        elif app.currWave == 3:
            msg = 'Jellyfish will shock your line!!'
            createJellyfish(app)
        elif app.currWave == 4:
            msg = 'Things are speeding up!'
        app.floaters.append(floater.floatingText(app.width,app.height//2,msg))
    # adjust spawn ratio
    if app.currWave == 2:
        app.spawnRatio.extend(['bigFish','bigFish','shark','shark',
                                'fish','fish','fastShark'])
    elif app.currWave == 3:
        app.spawnRatio.extend(['jellyfish','jellyfish','biggerFish','fish',
                                'bigFish','biggerFish','biggerFish','fastShark'])
    else:
        createExtraHook(app)

######### stylization

# returns a list of files in a path (from cs15112 S20 course notes)
def listFiles(path):
    if os.path.isfile(path):
        return [path]
    else:
        files = []
        for filename in os.listdir(path):
            files += listFiles(path + "/" + filename)
        return files

### game mode stylization  

def drawHook(app,canvas):
    img = Image.open('images/static/hook.png')
    img = img.resize((15,15))
    canvas.create_image(app.hX, app.hY, image=ImageTk.PhotoImage(img))

def drawWater(app,canvas):
    img = Image.open('images/static/background.png')
    
    waterDepth = app.height - app.waterHeight
    img = img.resize((app.width,waterDepth+app.height//6))
    canvas.create_image(0, app.waterHeight, anchor=NW, 
    image=ImageTk.PhotoImage(img))

def drawSky(app,canvas):
    img = Image.open('images/static/sky.png')
    img = img.resize((app.width,app.height))
    canvas.create_image(0,-300,anchor=NW,image=ImageTk.PhotoImage(img))

def drawBoat(app,canvas):
    img = Image.open('images/static/boat.png')
    width, height = img.size
    canvas.create_image(app.hX+40,app.waterHeight+70,anchor=SE,
                        image=ImageTk.PhotoImage(img))

def drawStats(app,canvas):
    # draw score
    canvas.create_text(app.width//30,app.height//15, 
        text=f'score: {app.score}',font='Fixedsys 10',fill='gray',anchor=W)
    # draw lives
    canvas.create_text(app.width//30,app.height//15+20, 
        text=f'hooks remaining: {app.lives}',font='Fixedsys 10',
        fill='gray',anchor=W)
    if app.onLine != None and app.currMeter == None:
        canvas.create_text(app.hX+100,app.height//15,
        text='Reel up and click to catch it!',
        font='Fixedsys 10',fill='gray',anchor=W)
    # draw pause instructions
    if app.gameOver == False:
        pauseMsg = "press 'p' to pause"
        if app.isPaused == True:
            pauseMsg = "press 'p' to unpause"
        canvas.create_text(app.width-20,app.height-20, 
            text=pauseMsg,font='Fixedsys 10',
            fill='dark gray',anchor=SE)

def drawShock(app,canvas):
    canvas.create_rectangle(app.hX-1,app.hMargin,
    app.hX+1,app.hY,fill='light blue',width=0)
    if app.time-app.timeShocked > 700:
        app.isShocking = False

### draw pop-up screens screens

# draws a pop-up background
def reactToButtons(app,event):
    if app.helpButton.isClicked(event.x,event.y):
        app.drawInstructions = True
    elif app.homeButton.isClicked(event.x,event.y):
        app.app.setActiveMode(app.app.homeScreen)
    elif app.restartButton.isClicked(event.x,event.y):
        if app.__class__.__name__ == 'gameMode':
            app.app.gameMode = gameMode()
            app.app.setActiveMode(app.app.gameMode)
        elif app.__class__.__name__ == 'clickToCatch':
            app.app.clickToCatchMode = clickToCatch()
            app.app.setActiveMode(app.app.clickToCatchMode)
        elif app.__class__.__name__ == 'expertMode':
            app.app.expertMode = expertMode()
            app.app.setActiveMode(app.app.expertMode)
    elif app.drawInstructions == True and \
        app.backButton.isClicked(event.x,event.y) == True:
        app.drawInstructions = False

def drawPopUp(app,canvas,cx,cy):
    r = (app.height//2) - 20
    canvas.create_oval(cx-r,cy-r,cx+r,cy+r,fill='white',width=0)

def drawGameOver(app,canvas,cx,cy):
    # background, title, and subtitles
    drawPopUp(app,canvas,cx,cy)
    d = (app.height) - 10
    img = Image.open('images/static/endgame.png')
    img = img.resize((d,d))
    canvas.create_image(cx,cy,image=ImageTk.PhotoImage(img))
    canvas.create_text(cx,cy-150,text='GAME OVER',font='Fixedsys 60',fill='red')
    canvas.create_text(app.width//2,app.height//2-100,
    text=f'your score: {app.score}',font='Fixedsys 20',fill='dark blue')
    
    oldScore = readFile("highScore.txt")
    name,score = oldScore.split(";")

    canvas.create_text(app.width//2,app.height//2-70,
    text=f'high score: {score}',font='Fixedsys 15',fill='dark blue')

    canvas.create_text(app.width//2,app.height//2-50,
    text=f'{name} is the reigning champion!',font='Fixedsys 10',fill='dark blue')

    # draw buttons
    app.helpButton = buttons.Button(cx+80,cy,30,'?')
    app.helpButton.msgSize = 25
    app.helpButton.draw(canvas)

    app.restartButton = buttons.Button(cx-80,cy,30,'restart')
    app.restartButton.draw(canvas)

    app.homeButton = buttons.Button(cx,cy,30,'home')
    app.homeButton.draw(canvas) 

def drawPause(app,canvas,cx,cy):
    # background and title
    drawPopUp(app,canvas,cx,cy)
    canvas.create_text(cx,cy-app.width//10,text='PAUSED',
        font='Fixedsys 60',fill='dark blue')
    
    # draw buttons
    app.helpButton = buttons.Button(cx,cy,30,'?')
    app.helpButton.msgSize = 25
    app.helpButton.draw(canvas)

    app.restartButton = buttons.Button(cx,cy+80,30,'restart')
    app.restartButton.draw(canvas)

    app.homeButton = buttons.Button(cx,cy+160,30,'home')
    app.homeButton.draw(canvas)  

def drawInstructions(app,canvas,cx,cy):
    drawPopUp(app,canvas,cx,cy)

    # draw back button
    app.backButton = buttons.Button(cx,cy-250,15,'X')
    app.backButton.msgSize = 15
    app.backButton.color = 'light blue'
    app.backButton.draw(canvas) 

    canvas.create_text(cx-app.backButton.msgSize,cy,font='Fixedsys',
    fill='dark blue',text=\
    """                        THINGS TO AVOID


        Trash...........debris can scare fish off your line

        Sharks..........if hooked will break your line

        Hungry Sharks...will swim toward hooked fish

        Jellyfish.......can shock and break your whole line
    

                        THINGS TO CATCH


        Fish............catch one of these for some points   

        Big Fish........only bites small fish, a lot of points

        Bigger Fish.....only bites big fish, massive points

        Extra Hooks.....rare, but essential!
    """)

######## click to catch functions

def createHookMeter(app): 
    x = app.hX+100
    y = app.waterHeight-50
    width = 200
    minW,maxW = app.aboutToCatch.getDifficulty(width,app)
    greenWidth = random.randint(minW,maxW)  
    speed = random.randint(app.aboutToCatch.weight,app.aboutToCatch.weight*3)
    app.currMeter = HookMeter(x,y,greenWidth,speed,width)
    
class HookMeter(object):
    def __init__(self,x,y,greenWidth,speed,width=200,direction=1,height=20):
        # meter parameters
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.greenWidth = greenWidth
        self.gdx = (self.width-self.greenWidth)//2 # red space of meter width
        
        # arrow parameters
        self.speed = speed
        self.direction = direction
        self.aX = random.randint(self.x,self.x+self.width) # arrow start x
        self.aP0 = (self.aX,self.y)
        self.aP1 = (self.aX+15,self.y+15)
        self.aP2 = (self.aX-15,self.y+15)
        
    def draw(self,canvas):
        # draw instruction
        canvas.create_text(self.x-60,self.y-(self.height+40),
        text='click the fish at the right time to hook it!',
        font='Fixedsys 10',fill='gray',anchor=W)
        # draw negative space
        canvas.create_rectangle(self.x,self.y,self.x+self.width,
            self.y-self.height,fill='pink',width=0)
        #draw positive space
        canvas.create_rectangle(self.x+self.gdx,self.y,
            self.x+self.width-self.gdx,self.y-self.height,
            fill='light green',width=0)
        # draw arrow
        canvas.create_polygon(self.aP0,self.aP1,self.aP2,fill='gray')
    
    def moveArrow(self):
        self.aX += (self.speed*self.direction)
        self.aP0 = (self.aX,self.y)
        self.aP1 = (self.aX+15,self.y+15)
        self.aP2 = (self.aX-15,self.y+15)
        if self.aX >= self.x+self.width:
            self.direction *= -1
            self.aX = self.x+self.width
        if self.x >= self.aX:
            self.direction *= -1
            self.aX = self.x
    
    def inGreen(self):
        minX = self.x + self.gdx
        maxX = minX + self.greenWidth
        return minX < self.aX and self.aX < maxX

######## high score info

# from 15112 course website: basic file IO
def readFile(path):
    with open(path, "rt") as f:
        return f.read()
# from 15112 course website: basic file IO
def writeFile(path, contents):
    with open(path, "wt") as f:
        f.write(contents)

# checks if there is a new high score and updates it if so
def newHighScore(app):
    oldScore = readFile("highScore.txt")
    _,score = oldScore.split(";")
    if app.score > int(score):
        newName = app.getUserInput('New HighScore! Enter your name!!') 
        newBestPlayer = f'{newName};{app.score}'
        writeFile("highScore.txt",newBestPlayer)




