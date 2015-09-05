from visual import *

ctable = [color.yellow,color.green,color.cyan,color.magenta]

SIZE = int(sys.argv[1]) if len(sys.argv) > 1 else 4
SPACING = .5
XOFFSET = arange(0, (SIZE+SPACING)*SIZE, SIZE+SPACING)

def draw2Dgrid(x,y,z,col):
    length = 1.*SIZE
    rad = 0.02
    for i in range(1,SIZE):
        cylinder(pos=(i+x,0+y,0+z),axis=(0,length,0),radius=rad,color=col)
        cylinder(pos=(0+x,i+y,0+z),axis=(length,0,0),radius=rad,color=col)

def draw2D():
    for i in range(SIZE):
        draw2Dgrid(i*(SIZE+SPACING),0,0,ctable[i])

def drawlabels(positions):
    for i in range(SIZE):
        for j in range(SIZE):
            for k in range(SIZE):
                label(pos=(i+SPACING+XOFFSET[k],j+SPACING,0), text=str(i)+', '+str(j)+', '+str(k), height=14)

def initializewindow():
    scene.title = '3D Tic-Tac-Toe'
    scene.autocenter = True
    #scene.fullscreen = True
    scene.userzoom = False
    scene.lights = [distant_light(direction=(0.22, -0.44, 0.88), color=color.gray(0.8)), distant_light(direction=(-0.88, 0.22, -0.44), color=color.gray(0.3))]

initializewindow()
draw2D()
drawlabels(zeros((SIZE,SIZE,SIZE)))
