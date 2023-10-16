#################################################
# buttons.py
#
# Your name: Jason Garwood
# Your andrew id: jgarwood
#################################################
# code defining button objects and associated functions
#################################################################

import functions, os
from cmu_112_graphics import *
from tkinter import *
from PIL import Image

#################################################################

class Button(object):
    def __init__(self,cx,cy,r,msg):
        self.cx,self.cy = cx,cy
        self.r = r
        self.msg = msg
        self.msgSize = int(self.r*(3/10))
        self.color = 'light blue'
        self.txtColor = 'dark blue'
        self.isActive = None # a boolean for 'switch' buttons

    def draw(self,canvas):
        canvas.create_oval(self.getBounds(),fill=self.color,width=0) 
        
        if self.msg == 'home':
            img = Image.open('images/static/home.png')
            img = img.resize((self.r,self.r))
            canvas.create_image(self.cx,self.cy,anchor=CENTER,
                image=ImageTk.PhotoImage(img))
        elif self.msg == 'restart':
            img = Image.open('images/static/restart.png')
            img = img.resize((self.r,self.r))
            canvas.create_image(self.cx,self.cy,anchor=CENTER,
                image=ImageTk.PhotoImage(img))
        else:
            canvas.create_text(self.cx,self.cy,font=f'Fixedsys {self.msgSize}',
                text=self.msg,fill=self.txtColor)

    def getBounds(self):
        x0 = self.cx-self.r
        y0 = self.cy-self.r
        x1 = self.cx+self.r
        y1 = self.cy+self.r
        return x0,y0,x1,y1

    def isClicked(self,x,y):
        return functions.distance(x,y,self.cx,self.cy) < self.r
        
    def drawHighlight(self,canvas):
        if self.isActive == True:
            hWidth = 5 # the size of the button highlight
            x0,y0,x1,y1 = self.getBounds()
            canvas.create_oval(x0-hWidth,y0-hWidth,x1+hWidth,y1+hWidth,
                fill='green',width=0)