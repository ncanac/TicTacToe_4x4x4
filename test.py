from __future__ import division
from visual import *
from visual.controls import *

def messingaround():
    sphere(pos=(.5,.5,.5),radius=.4,color=color.blue,opacity=.5)
    sphere(pos=(1.5,1.5,1.5),radius=.4,color=color.red,opacity=.5)

def draw3Dgrid():
    length = 3
    rad = 0.01
    step = 1
    col = color.green
    
    for i in range(1, length):
        for j in range(1, length):
            cylinder(pos=(0,i,j),axis=(length,0,0),radius=rad,color=col)
            cylinder(pos=(j,i,0),axis=(0,0,length),radius=rad,color=col)
            cylinder(pos=(j,0,i),axis=(0,length,0),radius=rad,color=col)

def menu():
    c=controls(title='Menu',x=0,y=0,width=scene.width,height=100,range=50)
    b=button(pos=(0,0),width=60,height=60,text='Click me')

scene.autocenter=True
scene.autoscale = True
#scene.userzoom = False
draw3Dgrid()
messingaround()
menu()

