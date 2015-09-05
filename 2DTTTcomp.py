#from __future__ import division
from visual import *
import time
import ai2d

def draw2Dgrid():
    step = 1.
    length = 3.*step
    rad = 0.01
    col = color.green
    
    for i in range(1,3):
        cylinder(pos=(i*step,0,0),axis=(0,length,0),radius=rad,color=col)
        cylinder(pos=(0,i*step,0),axis=(length,0,0),radius=rad,color=col)

def checkwin(positions):
    # check diagonals
    if trace(positions) == 3 or trace(rot90(positions)) == 3:
        return 1    # Blue player wins!
    if trace(positions) == -3 or trace(rot90(positions)) == -3:
        return -1   # Red player wins!
    # check rows
    for i in range(3):
        if sum(positions[i,:]) == 3 or sum(positions[:,i]) == 3:
            return 1    # Blue player wins!
        elif sum(positions[i,:]) == -3 or sum(positions[:,i]) == -3:
            return -1   # Red player wins!

def repeat(x, y, positions):
    return False if positions[x,y] == 0 else True

#def compmoverand(positions):
#    free = []
#    for i in range(3):
#        for j in range(3):
#            if positions[i,j] == 0:
#                free.append((i,j))
#    return free[random.randint(len(free))]

def play():
    turn = [-1,1][random.randint(2)]
    numturns = 0
    positions = zeros((3,3))
    winner = 0
    while not winner and numturns < 9:
        rate(30)
        if turn == -1:
            #time.sleep(1)   # Pretend to be thinking
            numturns += 1
            pos = ai2d.move(positions)
            #print pos
            positions[pos[0],pos[1]] = turn
            l = .8
            loc = (pos[0]+.5-l/2.,pos[1]+.5-l/2.,0)
            cylinder(pos=loc,axis=(l,l,0),radius=.03,color=color.red)
            loc = (pos[0]+.5+l/2.,pos[1]+.5-l/2.,0)
            cylinder(pos=loc,axis=(-l,l,0),radius=.03,color=color.red)
            winner = checkwin(positions)
            turn *= -1
        elif scene.mouse.clicked:
            m = scene.mouse.getclick()
            if m.pos[0] >= 0 and m.pos[0] <= 3 and m.pos[1] >= 0 and m.pos[1] <= 3 and not repeat(int(m.pos[0]),int(m.pos[1]),positions):
                numturns += 1
                #col = color.blue if turn == 1 else color.red
                loc = (floor(m.pos[0])+.5,floor(m.pos[1])+.5,0)
                positions[int(loc[0]),int(loc[1])] = turn
                ring(pos=loc,axis=(0,0,1),radius=.4,color=color.blue)
                turn *= -1
                winner = checkwin(positions)
    if winner == 1:
        label(pos=scene.center,text='Blue player wins!',height=scene.height/20.)
    elif winner == -1:
        label(pos=scene.center,text='Red player wins!',height=scene.height/20.)
    else:
        label(pos=scene.center,text='No one wins!',height=scene.height/20.)

def main():
    scene.title = 'Tic-Tac-Toe'
    scene.autocenter = True
    scene.userspin = False
    while 1:
        draw2Dgrid()
        play()
        scene.mouse.getclick()
        for obj in scene.objects:
            obj.visible = 0

main()


