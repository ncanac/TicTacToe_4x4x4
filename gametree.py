from __future__ import division
from visual import *
import sys
import aigametree

ctable = [color.yellow,color.green,color.cyan,color.magenta]

SIZE = 3
SPACING = .5
XOFFSET = arange(0, (SIZE+SPACING)*SIZE, SIZE+SPACING)

# Erases the screen
def erase():
    for obj in scene.objects:
        obj.visible = 0

# Draws 2D grids
def draw2D():
    for i in range(SIZE):
        draw2Dgrid(i*(SIZE+SPACING),0,0,ctable[i])

# Draws a 2D grid at coordinates (x,y,z)
def draw2Dgrid(x,y,z,col):
    length = 1.*SIZE
    rad = 0.02
    for i in range(1,SIZE):
        cylinder(pos=(i+x,0+y,0+z),axis=(0,length,0),radius=rad,color=col)
        cylinder(pos=(0+x,i+y,0+z),axis=(length,0,0),radius=rad,color=col)

# Populates 2D board with spheres with locations given by positions array
def draw2Dspheres(positions):
    for i in range(SIZE):
        for j in range(SIZE):
            for k in range(SIZE):
                if positions[i,j,k] == 1:
                        sphere(pos=(i+SPACING+XOFFSET[k],j+SPACING,0),radius=.4,color=color.blue)
                elif positions[i,j,k] == -1:
                        sphere(pos=(i+SPACING+XOFFSET[k],j+SPACING,0),radius=.4,color=color.red)

# Draws a 3D grid
SCALE = 1.5
def draw3Dgrid():
    SCALE = 1.5
    length = SIZE*SCALE
    rad = 0.02
    for i in range(SIZE):
        for j in range(1, SIZE):
            cylinder(pos=(j*SCALE,0.,i*SCALE),axis=(0.,length,0.),radius=rad,color=ctable[i])
            cylinder(pos=(0.,j*SCALE,i*SCALE),axis=(length,0.,0.),radius=rad,color=ctable[i])

# Populates 3D board with spheres with locations given by positions array
def draw3Dspheres(positions):
    SCALE = 1.5
    for i in range(SIZE):
        for j in range(SIZE):
            for k in range(SIZE):
                if positions[i,j,k] == 1:
                    sphere(pos=((i+SPACING)*SCALE,(j+SPACING)*SCALE,k*SCALE),radius=.4*SCALE,color=color.blue)
                elif positions[i,j,k] == -1:
                    sphere(pos=((i+SPACING)*SCALE,(j+SPACING)*SCALE,k*SCALE),radius=.4*SCALE,color=color.red)

# Checks to see if a piece has already been placed at position (x,y,z)
# Returns False is no piece there, true otherwise
def repeat(x, y, z, positions):
    return False if positions[x,y,z] == 0 else True

# Checks for a mouse click. If True, makes take appropriate action (place a piece or do nothing)
def move(positions, numturns, turn):
    xdivs = arange(SIZE+SPACING, (SIZE+SPACING)*(SIZE+1), SIZE+SPACING)
    m = scene.mouse.getclick()
    x, y = m.pos[0], m.pos[1]
    k = where(xdivs>x)[0][0]    # z index
    xoff = XOFFSET[k]
    if x-xoff >= 0 and x-xoff <= SIZE and y >= 0 and y <= SIZE:
        i = int(x-xoff)
        j = int(y)
        if not repeat(i,j,k,positions):
            positions[i,j,k] = turn
            numturns += 1
            col = color.blue if turn == 1 else color.red
            sphere(pos=(i+SPACING+xoff,j+SPACING,0),radius=.4,color=col)
            turn *= -1
    return positions, numturns, turn

# Checks to see if view toggle button 'v' has been pressed. If True, changes view from 2D to 3D or vice versa.
def changemode(mode, positions):
    erase()
    if mode == 1:   # Switch to 3D view
        scene.userspin = True
        scene.forward = (0,1,0)
        scene.up = (0,0,1)
        draw3Dgrid()
        draw3Dspheres(positions)
        mode *= -1
    else:           # Swtich to 2D view
        scene.userspin = False
        scene.forward = (0,0,-1)
        scene.up = (0,1,0)
        draw2D()
        draw2Dspheres(positions)
        mode *= -1
    return mode

# Checks the board to see if there are 4 in a row anywhere
def checkwin(positions):
    dim = 3
    # Check diagonals in planes
    for i in range(dim-1):
        for j in range(i+1,dim):
            if len(where(trace(positions, axis1=i, axis2=j)==SIZE)[0]) > 0 or len(where(trace(rot90(swapaxes(swapaxes(positions, axis1=0, axis2=i), axis1=1, axis2=j)))==SIZE)[0]) > 0:
                return 1
            if len(where(trace(positions, axis1=i, axis2=j)==-1*SIZE)[0]) > 0 or len(where(trace(rot90(swapaxes(swapaxes(positions, axis1=0, axis2=i), axis1=1, axis2=j)))==-1*SIZE)[0]) > 0:
                return -1
    # Check rows
    for i in range(dim):
        if len(where(positions.sum(axis=i).flatten()==SIZE)[0]) > 0:
            return 1
        if len(where(positions.sum(axis=i).flatten()==-1*SIZE)[0]) > 0:
            return -1
    # Check other diagonals
    tot = [0, 0, 0, 0]
    for i in range(SIZE):
        tot[0] += positions[i,i,i]
        tot[1] += positions[i,SIZE-1-i,i]
        tot[2] += positions[SIZE-1-i,i,i]
        tot[3] += positions[SIZE-1-i,SIZE-1-i,i]
    for i in range(len(tot)):
        if tot[i] == SIZE:
            return 1
        if tot[i] == -1*SIZE:
            return -1

#def play():
#    draw2D()
#    scene.userspin = False
#    mode, numturns, turn = 1, 0, [-1, -1][random.randint(2)]
#    positions = zeros((SIZE,SIZE,SIZE))
#    winner = 0
#    while not winner and numturns < 64:
#        rate(30)
#        if turn == -1:
#            pos = aigametree.move(positions)
#            #print pos
#            positions[pos[0],pos[1],pos[2]] = turn
#            sphere(pos=(pos[0]+SPACING+XOFFSET[pos[2]],pos[1]+SPACING,0),radius=.4,color=color.red)
#            winner = checkwin(positions)
#            turn *= -1
#        elif scene.kb.keys and scene.kb.getkey() == 'v':
#            mode = changemode(mode, positions)
#        elif mode == 1 and scene.mouse.clicked:   # 2D mode and mouse clicked
#            positions, numturns, turn = move(positions, numturns, turn)
#            winner = checkwin(positions)
#    return winner

def test():
    bluewins = 0
    redwins = 0
    draws = 0
    for i in range(3):
        for j in range(3):
            for k in range(3):
                if (i,j,k) != (1,1,1):
                    for l in range(3):
                        for m in range(3):
                            for n in range(3):
                                if (l,m,n) != (1,1,1) and (l,m,n) != (i,j,k):
                                    positions = zeros((3,3,3))
                                    positions[1,1,1] = -1
                                    positions[i,j,k] = 1
                                    positions[l,m,n] = -1
                                    turn = 1
                                    winner = 0
                                    numturns = 3
                                    while not winner and numturns < 27:
                                        if turn == -1:
                                            pos = aigametree.move(positions)
                                            positions[pos[0],pos[1],pos[2]] = turn
                                        elif turn == 1:
                                            pos, move = aigametree.canwin(positions)
                                            #print pos
                                            positions[pos[0],pos[1],pos[2]] = turn
                                        winner = checkwin(positions)
                                        turn *= -1
                                        numturns += 1
                                    if winner == -1:
                                        redwins += 1
                                    elif winner == 1:
                                        bluewins += 1
                                    elif winner == 0:
                                        draws += 1
    print redwins
    print bluewins
    print draws

def initializewindow():
    scene.title = '3D Tic-Tac-Toe'
    scene.autocenter = True
    #scene.fullscreen = True
    scene.userzoom = False
    scene.lights = [distant_light(direction=(0.22, -0.44, 0.88), color=color.gray(0.8)), distant_light(direction=(-0.88, 0.22, -0.44), color=color.gray(0.3))]

def main():
    initializewindow()
    while 1:
        play()
        scene.mouse.getclick()
        erase()

test()
