#################################################
# floater.py
#
# Your name: Jason Garwood
# Your andrew id: jgarwood
#################################################
#code defining floater objects and functions associated with them
#################################################################

import functions, os
from cmu_112_graphics import *
from tkinter import *
from PIL import Image

#################################################################

class floater(object):
    def __init__(self,x,y,dx,speed,collisionR=20):
        self.x = x
        self.y = y
        self.dx = dx
        self.speed = speed
        self.collisionR = collisionR 
        self.onLine = False
        self.isCatchable = False
        
    def move(self, app):
        self.x += (self.dx * self.speed) 
        # remove from app if out of bounds
        self.removeOffScreen(app)
        # test for and react to collisions with line/hook
        self.testForCollision(app)
    
    # remove from data if out of canvas bounds 
    def removeOffScreen(self,app):
        if self.x < (-2*self.collisionR) \
            or self.x > app.width +((2*self.collisionR)):
            app.floaters.remove(self)

    # return True if an object is colliding with the line
    def isCollidingLine(self,app):
        collisionDist = functions.distance(self.x,0,app.hX,0)
        if collisionDist < (self.speed*2) and self.y < app.hY:
            return True
        return False

    # return True if an object is colliding with the hook
    def isCollidingHook(self,app):
        if functions.distance(self.x,self.y,app.width//2,app.hY)\
            < self.collisionR:
            return True
        return False

    # test for collisions with hook/line and react respectivly
    def testForCollision(self,app):
        if app.hasHook and self.isCollidingHook(app) and self.onLine == False:
            self.reactToHook(app)
        if app.hasHook and self.isCollidingLine(app):
            self.reactToLine(app)

    # do nothing if not overwritten in subclass
    def reactToHook(self,app):
        pass
    def reactToLine(self,app):
        pass

    def isClicked(self,x,y):
        return functions.distance(x,y,self.x,self.y) < self.collisionR

    # takes in an image and a desired size and sets that image as the instance
    def setImage(self,image,size):
        self.image = Image.open(image)
        self.image = self.image.resize(size)
        if self.dx > 0 :
            self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)            

    def draw(self,canvas):
        canvas.create_image(self.x,self.y,image=ImageTk.PhotoImage(self.image))
        
#### fish classes

class Fish(floater):
    def __init__(self,x,y,dx,speed,collisionR=20,scoreValue=100):
        super().__init__(x,y,dx,speed,collisionR)
        self.scoreValue = scoreValue
        self.isCatchable = True 
        self.weight = 4
        # stylize object
        self.imgList = functions.listFiles('images/fish')
        self.imgIndex = 0
        self.imageSize = (50,50)
        self.setImage(self.imgList[self.imgIndex],self.imageSize)

    # returns a tuple of the successfully hooked range
    def getDifficulty(self,width,app):
        maxW = width - (self.weight*self.speed)

        # keep range playable
        if maxW > width-20:
            maxW = width-20
        elif maxW < 30:
            maxW = 30
        minW = maxW//(self.weight//2)
        if minW < 10:
            minW = 10
        return (minW,maxW)

    # hook the fish and allow for reeling up
    def reactToHook(self,app):
        if app.onLine == None:
            # create fish meter
            if app.clickMode == True and \
                app.currMeter == None and self.isCatchable == True:
                self.initializeCatch(app)
            # hook the fish
            elif app.meterSuccess == True or app.clickMode == False:
                self.hookFish(app)
                if app.currWave > 3:
                    app.spawnRatio.extend(['bigFish'])              

    # sets a fish up to be caught
    def initializeCatch(self,app):
        app.aboutToCatch = self
        functions.createHookMeter(app)
        self.isCatchable = False

    def hookFish(self,app):
            app.onLine = self
            self.onLine = True
            self.x,self.y = app.hX,app.hY
            app.meterSuccess = False 
            self.trackLocation(app)

    # adjusts the spawn location based on where fish are being caught
    def trackLocation(self,app):
        # if caught at top make more likely to spawn at bottom
        if self.y < app.midWater:
            app.minSpawnY += 10
        # if caught at bottom make more likely to spawn at top
        else:
            app.maxSpawnY -= 10

        # if the spawn range is too small, the range increases accordingly 
        if app.maxSpawnY-app.minSpawnY < app.height//4:
            # increase the probability of spawning lower if caught at top
            if self.y < app.midWater:
                app.maxSpawnY += 30
                app.minSpawnY -= 20
            # increase the probability of spawning higher if caught at bottom
            else:
                app.maxSpawnY -= 30
                app.minSpawnY += 20

        # ensure in the water
        if app.maxSpawnY > app.height+100:
            app.maxSpawnY = app.height+100
        if app.minSpawnY < app.waterHeight+30:
            app.minSpawnY = app.waterHeight+30
            
class bigFish(Fish):
    def __init__(self,x,y,dx,speed,collisionR=40,scoreValue=400):
        super().__init__(x,y,dx,speed,collisionR,scoreValue)
        self.weight = 6
        
        # stylize object
        self.imgList = functions.listFiles('images/bigFish')
        self.imgIndex = 0
        self.imageSize = (125,125)
        self.setImage(self.imgList[self.imgIndex],self.imageSize)

    # if there is a fish on the line, eat it and get caught    
    def reactToHook(self,app):
        if app.onLine.__class__.__name__ == 'Fish':
            # create fish meter
            if app.clickMode == True and \
                app.currMeter == None and self.isCatchable == True:
                self.initializeCatch(app)
            # hook the fish
            elif app.meterSuccess == True or app.clickMode == False:
                app.floaters.remove(app.onLine)
                self.hookFish(app)
                if app.currWave > 3:
                    app.spawnRatio.extend(['biggerFish','biggerFish','fish'])  
      
class biggerFish(Fish):
    def __init__(self,x,y,dx,speed,collisionR=70,scoreValue=1000):
        super().__init__(x,y,dx,speed,collisionR,scoreValue)
        self.weight = 8
        
        # stylize object
        self.imgList = functions.listFiles('images/biggerFish')
        self.imgIndex = 0
        self.imageSize = (300,200)
        self.setImage(self.imgList[self.imgIndex],self.imageSize)

    # if there is a big fish on the line, eat it and get caught
    def reactToHook(self,app):
        # create fish meter
        if app.onLine.__class__.__name__ == 'bigFish':
            if app.clickMode == True and \
                app.currMeter == None and self.isCatchable == True:
                self.initializeCatch(app)
            # hook the fish
            elif app.meterSuccess == True or app.clickMode == False:
                app.floaters.remove(app.onLine)
                self.hookFish(app)
                if app.currWave > 3:
                    app.spawnRatio.extend(['fish','bigFish'])
   
#### enemy classes

class Trash(floater):
    def __init__(self,x,y,dx,speed,collisionR=60):
        super().__init__(x,y,dx,speed,collisionR)

        # stylize object
        self.imgList = functions.listFiles('images/trash')
        self.imgIndex = 0
        self.imageSize = (150,150)
        self.setImage(self.imgList[self.imgIndex],self.imageSize)
    
    # if a fish is on line scare it off
    def reactToHook(self,app):
        if app.onLine != None:
            currFish = app.onLine
            app.floaters.remove(app.onLine)
            currFish.onLine = False
            app.onLine.speed *= 2
            app.floaters.append(currFish)
            app.onLine = None

# can break hook off line      
class Shark(floater):
    def __init__(self,x,y,dx,speed,collisionR=60):
        super().__init__(x,y,dx,speed,collisionR)
        self.speed *= 1.5

        # stylize object
        self.imgList = functions.listFiles('images/shark')
        self.imgIndex = 0
        self.imageSize = (400,400)
        self.setImage(self.imgList[self.imgIndex],self.imageSize)

    # remove from data if out of canvas bounds 
    def removeOffScreen(self,app):        
        if self.x < (-2*self.collisionR) \
            or self.x > app.width +((2*self.collisionR)):
            # increase spawn ratio of enemy if it passes under the boat
            if app.currWave == 4:
                    if self.__class__.__name__ == 'shark':
                        app.sharkCount += 1
                        if app.sharkCount % app.enemyRate == 0:
                            app.spawnRatio.extend(['shark'])
            app.floaters.remove(self)

    # eat the fish and hook, breaking the line
    def reactToHook(self,app):
        if app.lives == 0:
            functions.newHighScore(app)
            app.gameOver = True
        # if fish is online eat it! Break the fishing line too!!
        elif app.onLine != None:
            app.floaters.remove(app.onLine)
            app.onLine = None
            app.hasHook = False
        else:
            app.hasHook = False

        # if hit make less likely to spawn
        if app.currWave == 4 and app.spawnRatio.count('shark') > 1:
            app.spawnRatio.remove('shark')

# hones in on the line if there is a fish on it
class FastShark(Shark):
    def __init__(self,x,y,dx,speed,collisionR=60):
        super().__init__(x,y,dx,speed,collisionR)

        # stylize object
        self.imgList = functions.listFiles('images/fastShark')
        self.imgIndex = 0
        self.imageSize = (200,90)
        self.setImage(self.imgList[self.imgIndex],self.imageSize)

    # moves towards a hooked fish if it has not passed it 
    def move(self,app):
        # determine if a fish is visible to the fastShark and react accordingly
        if app.onLine != None and app.hY > app.waterHeight:
            fishIsVisible = False
            if self.dx > 0:
                if self.x < app.hX:
                    fishIsVisible = True
            else:
                if self.x > app.hX:
                    fishIsVisible = True
            # if the shark can see a hooked fish, attack it
            if fishIsVisible == True:
                self.x += (self.dx * self.speed)
                if app.hY > self.y:
                    self.y += self.speed
                elif app.hY < self.y:
                    self.y -= self.speed
                
                # test for collision and out of bounds
                self.removeOffScreen(app)
                self.testForCollision(app)
                return
        super().move(app)

    # remove from data if out of canvas bounds  
    def removeOffScreen(self,app):        
        if self.x < (-2*self.collisionR) \
                or self.x > app.width +((2*self.collisionR)):
            # increase spawn ratio of enemy if it passes under the boat
            if app.currWave == 4:
                    if self.__class__.__name__ == 'fastShark':
                        app.fastSharkCount += 1
                        if app.fastSharkCount % app.enemyRate == 0:
                            app.spawnRatio.extend(['fastShark'])
            
            app.floaters.remove(self)

    # eat the fish and hook, breaking the line
    def reactToHook(self,app):
        if app.lives == 0:
            functions.newHighScore(app)
            app.gameOver = True
        # if fish is online eat it! Break the fishing line too!!
        elif app.onLine != None:
            app.floaters.remove(app.onLine)
            app.onLine = None
            app.hasHook = False
        else:
            app.hasHook = False

        # if hit make less likely to spawn
        if app.currWave == 4 and app.spawnRatio.count('fastShark') > 1:
            app.spawnRatio.remove('fastShark')

# can shock line
class Jellyfish(floater):
    def __init__(self,x,y,dx,speed,collisionR=20):
       super().__init__(x,y,dx,speed,collisionR)

       # stylize object 
       self.imgList = functions.listFiles('images/jellyfish')
       self.imgIndex = 0
       self.imageSize = (100,100)
       self.setImage(self.imgList[self.imgIndex],self.imageSize)
    
    # shock the line, break the hook off, and scare the fish away!
    def reactToLine(self,app):
        # if a fish is on line, if so unhook it
        app.isShocking = True
        app.timeShocked = app.time
        if app.lives == 0:
            functions.newHighScore(app)
            app.gameOver = True   
        elif app.onLine != None:
            currFish = app.onLine
            app.floaters.remove(app.onLine)
            currFish.onLine = False
            app.onLine.speed *= 2
            app.floaters.append(currFish)
            app.onLine = None
            app.hasHook = False
        else:
            app.hasHook = False
        
        # if hit make less likely to spawn
        if app.currWave == 4 and app.spawnRatio.count('jellyfish') > 1:
            app.spawnRatio.remove('jellyfish')

    # remove from data if out of canvas bounds 
    def removeOffScreen(self,app):        
        if self.x < (-2*self.collisionR) \
            or self.x > app.width +((2*self.collisionR)):
            # increase spawn ratio of enemy if it passes under the boat
            if app.currWave == 4:
                    if self.__class__.__name__ == 'Jellyfish':
                        app.jellyCount += 1
                        if app.jellyCount % app.enemyRate == 0:
                            app.spawnRatio.extend(['jellyfish'])
            app.floaters.remove(self)

#### gameplay classes

class extraHook(floater):
    def __init__(self,x,y,dx,speed,collisionR=20):
        super().__init__(x,y,dx,speed,collisionR)

        # stylize object
        self.imgList = functions.listFiles('images/static/bonus.png')
        self.imgIndex = 0
        self.imageSize = (50,45)
        self.setImage(self.imgList[self.imgIndex],self.imageSize)

    # increase hooks remaining if caught
    def reactToHook(self,app):
        app.floaters.remove(self)
        app.lives += 1

class floatingText(floater):
    def __init__(self,x,y,message,dx=-1,speed=30,collisionR=450):
       super().__init__(x,y,dx,speed,collisionR)
       self.message = message
    def draw(self,canvas):
        canvas.create_text(self.x,self.y,text=self.message,
                           font='Fixedsys 24',fill='light blue',anchor=W)