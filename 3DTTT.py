from __future__ import division
from visual import *
import sys

ctable = [color.yellow,color.green,color.cyan,color.magenta]

SIZE = int(sys.argv[1]) if len(sys.argv) > 1 else 4
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
    if scene.mouse.clicked:
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

def checkwin(positions):
    # check plane diagonals
    for i in range(SIZE):
        if trace(positions[:,:,i]) == SIZE or trace(rot90(positions[:,:,i])) == SIZE:
            return 1    # Blue player wins!
        if trace(positions[:,:,i]) == -1*SIZE or trace(rot90(positions[:,:,i])) == -1*SIZE:
            return -1   # Red player wins!
    for i in range(SIZE):
        if trace(positions[i,:,:]) == SIZE or trace(rot90(positions[i,:,:])) == SIZE:
            return 1    # Blue player wins!
        if trace(positions[i,:,:]) == -1*SIZE or trace(rot90(positions[i,:,:])) == -1*SIZE:
            return -1   # Red player wins!
    for i in range(SIZE):
        if trace(positions[:,i,:]) == SIZE or trace(rot90(positions[i,:,:])) == SIZE:
            return 1    # Blue player wins!
        if trace(positions[:,i,:]) == -1*SIZE or trace(rot90(positions[i,:,:])) == -1*SIZE:
            return -1   # Red player wins!
    # check rows
    for i in range(SIZE):
        for j in range(SIZE):
            if sum(positions[j,:,i]) == SIZE or sum(positions[:,j,i]) == SIZE:
                return 1    # Blue player wins!
            elif sum(positions[j,:,i]) == -1*SIZE or sum(positions[:,j,i]) == -1*SIZE:
                return -1   # Red player wins!
    for i in range(SIZE):
        for j in range(SIZE):
            if sum(positions[i,:,j]) == SIZE or sum(positions[i,j,:]) == SIZE:
                return 1    # Blue player wins!
            elif sum(positions[i,:,j]) == -1*SIZE or sum(positions[i,j,:]) == -1*SIZE:
                return -1   # Red player wins!
    for i in range(SIZE):
        for j in range(SIZE):
            if sum(positions[j,i,:]) == SIZE or sum(positions[:,i,j]) == SIZE:
                return 1    # Blue player wins!
            elif sum(positions[j,i,:]) == -SIZE or sum(positions[:,i,j]) == -1*SIZE:
                return -1   # Red player wins!
    # check other diagonals
    tot = 0
    for i in range(SIZE):
        tot += positions[i,i,i]
    if tot == SIZE:
        return 1
    if tot == -1*SIZE:
        return -1
        tot = 0
    tot = 0
    for i in range(SIZE):
        tot += positions[i,SIZE-1-i,i]
    if tot == SIZE:
        return 1
    if tot == -1*SIZE:
        return -1
        tot = 0
    tot = 0
    for i in range(SIZE):
        tot += positions[SIZE-1-i,SIZE-1-i,i]
    if tot == SIZE:
        return 1
    if tot == -1*SIZE:
        return -1
        tot = 0
    tot = 0
    for i in range(SIZE):
        tot += positions[SIZE-1-i,i,i]
    if tot == SIZE:
        return 1
    if tot == -1*SIZE:
        return -1

def play():
    draw2D()
    scene.userspin = False
    mode, numturns, turn = 1, 0, 1
    positions = zeros((SIZE,SIZE,SIZE))
    winner = 0
    while not winner and numturns < 64:
        rate(30)
        if scene.kb.keys:
            s = scene.kb.getkey()
            if s == 'v':
                mode = changemode(mode, positions)
        if mode == 1:   # 2D mode
            positions, numturns, turn = move(positions, numturns, turn)
            winner = checkwin(positions)
    if winner == 1:
        label(pos=scene.center,text='Blue player wins!',height=scene.height/20.)
    elif winner == -1:
        label(pos=scene.center,text='Red player wins!',height=scene.height/20.)
    key = 'a'
    while key != '\n':
        rate(30)
        if scene.kb.keys:
            key = scene.kb.getkey()
            if key == 'v':
                mode = changemode(mode, positions)
        while scene.mouse.clicked:
            scene.mouse.getclick()

def initializewindow():
    scene.title = '3D Tic-Tac-Toe'
    scene.autocenter = True
    scene.fullscreen = True
    scene.userzoom = False
    scene.lights = [distant_light(direction=(0.22, -0.44, 0.88), color=color.gray(0.8)), distant_light(direction=(-0.88, 0.22, -0.44), color=color.gray(0.3))]

def main():
    initializewindow()
    while 1:
        play()
        erase()

main()
