from numpy import *
from visual import *

DIM = 3

#def randmove(positions):
#    free = []
#    size = len(positions)
#    for i in range(size):
#        for j in range(size):
#            for k in range(size):
#                if positions[i,j,k] == 0:
#                    free.append((i,j,k))
#    print len(free)
#    return free[0]

#def randmove(positions):
#    free = []
#    size = len(positions)
#    for i in range(size):
#        for j in range(size):
#            for k in range(size):
#                if positions[i,j,k] == 0:
#                    free.append((i,j,k))
#    print type(free)
#    return free[0]

def checkdiagwin(positions, player):
    size = len(positions)
    offsets = [[0,0],[0,size-1],[size-1,0],[size-1,size-1]]
    tot = [0]*size
    pos = (-1,-1,-1)
    for i in range(size):
        for j in range(len(tot)):
            tot[i] += positions[abs(j-offsets[i][0]),abs(j-offsets[i][1]),j]
    for i in range(size):
        if tot[i] == (size-1)*player:
            for j in range(len(tot)):
                pos = (abs(j-offsets[i][0]),abs(j-offsets[i][1]),j)
                if positions[pos] == 0:
                    return pos
    return pos

def planediagwin(positions, player):
    size = len(positions)
    pos = (-1,-1,-1)
    for i in range(size):
        tot = [0,0]
        for j in range(size):
            tot[0] += positions[i,j,j]
            tot[1] += positions[i,j,size-1-j]
        if tot[0] == (size-1)*player:
            for j in range(size):
                pos = (i,j,j)
                if positions[pos] == 0:
                    return pos
        if tot[1] == (size-1)*player:
            for j in range(size):
                pos = (i,j,size-1-j)
                if positions[pos] == 0:
                    return pos
    for i in range(size):
        tot = [0,0]
        for j in range(size):
            tot[0] += positions[j,i,j]
            tot[1] += positions[j,i,size-1-j]
        if tot[0] == (size-1)*player:
            for j in range(size):
                pos = (j,i,j)
                if positions[pos] == 0:
                    return pos
        if tot[1] == (size-1)*player:
            for j in range(size):
                pos = (j,i,size-1-j)
                if positions[pos] == 0:
                    return pos
    for i in range(size):
        tot = [0,0]
        for j in range(size):
            tot[0] += positions[j,j,i]
            tot[1] += positions[j,size-1-j,i]
        if tot[0] == (size-1)*player:
            for j in range(size):
                pos = (j,j,i)
                if positions[pos] == 0:
                    return pos
        if tot[1] == (size-1)*player:
            for j in range(size):
                pos = (j,size-1-j,i)
                if positions[pos] == 0:
                    return pos
    return pos

def canwin(positions):
    pos = [-1]*DIM
    size = len(positions)
    for i in range(DIM):
        axwin = where(positions.sum(axis=i)==-1*(size-1))
        if len(axwin[0]) > 0:
            pos[(i+1)%DIM] = axwin[i%2][0]
            pos[(i+2)%DIM] = axwin[(i+1)%2][0]
            row = where(take(take(positions,[axwin[i%2][0]],axis=(i+1)%DIM),[axwin[(i+1)%2][0]],axis=(i+2)%DIM).flatten()==0)[0]
            if len(row) > 0:
                pos[i] = row[0]
                return tuple(pos), True
    pos = planediagwin(positions, -1)
    if sum(pos) >= 0:
        return tuple(pos), True
    pos = checkdiagwin(positions, -1)
    if sum(pos) >= 0:
        return tuple(pos), True
    return tuple(pos), False

def oppwin(positions):
    pos = [-1]*DIM
    size = len(positions)
    for i in range(DIM):
        axwin = where(positions.sum(axis=i)==size-1)
        if len(axwin[0]) > 0:
            #print i
            pos[(i+1)%DIM] = axwin[i%2][0]
            pos[(i+2)%DIM] = axwin[(i+1)%2][0]
            row = where(take(take(positions,[axwin[i%2][0]],axis=(i+1)%DIM),[axwin[(i+1)%2][0]],axis=(i+2)%DIM).flatten()==0)[0]
            if len(row) > 0:
                pos[i] = row[0]
                return tuple(pos), True
    pos = planediagwin(positions, 1)
    if sum(pos) >= 0:
        return tuple(pos), True
    pos = checkdiagwin(positions, 1)
    if sum(pos) >= 0:
        return tuple(pos), True
    return tuple(pos), False

def createfork(positions):
    size = len(positions[0])
    replace = where(positions==-1)
    posits = copy(positions)
    posits[replace[0],replace[1],replace[2]] = -2
    ax0 = where(posits.sum(axis=0)==-2*(size-2))
    ax1 = where(posits.sum(axis=1)==-2*(size-2))
    # Check for "row" forks
    for i in range(len(ax0[0])):
        for j in range(len(ax1[0])):
            if ax0[1][i] == ax1[1][j]:
                if positions[ax1[0][j],ax0[0][i],ax0[1][i]] == 0:
                    return (ax1[0][j],ax0[0][i],ax0[1][i])
    ax2 = where(posits.sum(axis=2)==-2*(size-2))
    for i in range(len(ax0[0])):
        for j in range(len(ax2[0])):
            if ax0[0][i] == ax2[1][j]:
                if positions[ax2[0][j],ax0[0][i],ax0[1][i]] == 0:
                    return (ax2[0][j],ax0[0][i],ax0[1][i])
    for i in range(len(ax1[0])):
        for j in range(len(ax2[0])):
            if ax1[0][i] == ax2[0][j]:
                if positions[ax2[0][j],ax2[1][j],ax1[1][i]] == 0:
                    return (ax2[0][j],ax2[1][j],ax1[1][i])
    # Check for 3D diagonal with anything else fork
    offsets = [[0,0],[0,size-1],[size-1,0],[size-1,size-1]]
    dtot = [0]*(2**(DIM-1))
    for i in range(len(dtot)):
        for j in range(size):
            dtot[i] += posits[abs(j-offsets[i][0]),abs(j-offsets[i][1]),j]
    for i in range(len(dtot)):
        if dtot[i] == (size-2)*-2:
            for j in range(size):
                pos = (abs(j-offsets[i][0]),abs(j-offsets[i][1]),j)
                if posits[pos] == 0:
                # Check each intersecting row
                    if sum(posits[pos[0],pos[1],:]) == (size-2)*-2 or sum(posits[pos[0],:,pos[2]]) == (size-2)*-2 or sum(posits[:,pos[1],pos[2]]) == (size-2)*-2:
                        return tuple(pos)
#                if pos[0] == 0 or pos[0] == size-1 or pos[1] == 0 or pos[1] == size-1:
#                 #Corner piece - must check plane diagonal too
#                    s = 0
#                    for k in range(size):
#                        s += posits[abs(pos[0]-offsets[i][0]),pos[1],k]
#                    if s == (size-2)*2:
#                        return tuple(pos)
#                    s = 0
#                    for k in range(size):
#                        s += posits[pos[0],abs(pos[1]-offsets[i][0]),k]
#                    if s == (size-2)*2:
#                        return tuple(pos)

    for i in range(size):
        tot = [0,0]
        for j in range(size):
            tot[0] += posits[i,j,j]
            tot[1] += posits[i,j,size-1-j]
        if tot[0] == (size-2)*-2:
            #print "Yay!"
            for j in range(size):
                if positions[(i,j,j)] == 0:
                    if sum(posits[i,j,:]) == (size-2)*-2 or sum(posits[i,:,j]) == (size-2)*-2 or sum(posits[:,j,j]) == (size-2)*-2:
                        return (i,j,j)
                    if j == 0 and i == 0:
                        s = 0
                        for k in range(size):
                            #sphere(pos=(k+SPACING+XOFFSET[k],i+SPACING,0),radius=.2,color=color.green)
                            s += posits[k,i,k]
                        if s == (size-2)*-2:
                            return (i,j,j)
                        s = 0
                        for k in range(size):
                            #sphere(pos=(k+SPACING+XOFFSET[i],k+SPACING,0),radius=.2,color=color.green)
                            s += posits[k,k,i]
                        if s == (size-2)*-2:
                            return (i,j,j)
                        if dtot[0] == (size-2)*-2:
                            return (i,j,j)
                    if j == 0 and i == size-1:
                        s = 0
                        for k in range(size):
                            #sphere(pos=(size-1-k+SPACING+XOFFSET[k],size-1-i+SPACING,0),radius=.2,color=color.green)
                            s += posits[size-1-k,size-1-i,k]
                        if s == (size-2)*-2:
                            return (i,j,j)
                        s = 0
                        for k in range(size):
                            #sphere(pos=(k+SPACING+XOFFSET[size-1-i],size-1-k+SPACING,0),radius=.2,color=color.green)
                            s += posits[k,size-1-k,size-1-i]
                        if s == (size-2)*-2:
                            return (i,j,j)
                        if dtot[2] == (size-2)*-2:
                            return (i,j,j)
                    if j == size-1 and i == 0:
                        #print (i, j, j)
                        s = 0
                        for k in range(size):
                            #sphere(pos=(size-1-k+SPACING+XOFFSET[k],size-1-i+SPACING,0),radius=.2,color=color.green)
                            s += posits[size-1-k,size-1-i,k]
                        if s == (size-2)*-2:
                            return (i,j,j)
                        s = 0
                        for k in range(size):
                            #sphere(pos=(size-1-k+SPACING+XOFFSET[size-1-i],k+SPACING,0),radius=.2,color=color.green)
                            s += posits[size-1-k,k,size-1-i]
                        if s == (size-2)*-2:
                            return (i,j,j)
                        if dtot[2] == (size-2)*-2:
                            return (i,j,j)
                    if j == size-1 and i == size-1:
                        s = 0
                        for k in range(size):
                            #sphere(pos=(k+SPACING+XOFFSET[k],i+SPACING,0),radius=.2,color=color.green)
                            s += posits[k,i,k]
                        if s == (size-2)*-2:
                            return (i,j,j)
                        s = 0
                        for k in range(size):
                            #sphere(pos=(k+SPACING+XOFFSET[i],k+SPACING,0),radius=.2,color=color.green)
                            s += posits[k,k,i]
                        if s == (size-2)*-2:
                            return (i,j,j)
                        if dtot[0] == (size-2)*-2:
                            return (i,j,j)
        if tot[1] == (size-2)*-2:
            #print "yay!"
            for j in range(size):
                if positions[(i,j,size-1-j)] == 0:
                    if sum(posits[i,j,:]) == (size-2)*-2 or sum(posits[i,:,size-1-j]) == (size-2)*-2 or sum(posits[:,j,size-1-j]) == (size-2)*-2:
                        return (i,j,size-1-j)
                    if j == 0 and i == 0:
                        s = 0
                        for k in range(size):
                            #sphere(pos=(size-1-k+SPACING+XOFFSET[k],i+SPACING,0),radius=.2,color=color.green)
                            s += posits[size-1-k,i,k]
                        if s == (size-2)*-2:
                            return (i,j,size-1-j)
                        s = 0
                        for k in range(size):
                            #sphere(pos=(k+SPACING+XOFFSET[size-1-i],k+SPACING,0),radius=.2,color=color.green)
                            s += posits[k,k,size-1-i]
                        if s == (size-2)*-2:
                            return (i,j,size-1-j)
                        if dtot[3] == (size-2)*-2:
                            return (i,j,size-1-j)
                    if j == 0 and i == size-1:
                        s = 0
                        for k in range(size):
                            #sphere(pos=(k+SPACING+XOFFSET[k],size-1-i+SPACING,0),radius=.2,color=color.green)
                            s += posits[k,size-1-i,k]
                        if s == (size-2)*-2:
                            return (i,j,size-1-j)
                        s = 0
                        for k in range(size):
                            #sphere(pos=(size-1-k+SPACING+XOFFSET[i],k+SPACING,0),radius=.2,color=color.green)
                            s += posits[size-1-k,k,i]
                        if s == (size-2)*-2:
                            return (i,j,size-1-j)
                        if dtot[1] == (size-2)*-2:
                            return (i,j,size-1-j)
                    if j == size-1 and i == 0:
                        s = 0
                        for k in range(size):
                            #sphere(pos=(k+SPACING+XOFFSET[k],size-1-i+SPACING,0),radius=.2,color=color.green)
                            s += posits[k,size-1-i,k]
                        if s == (size-2)*-2:
                            return (i,j,size-1-j)
                        s = 0
                        for k in range(size):
                            #sphere(pos=(k+SPACING+XOFFSET[i],size-1-k+SPACING,0),radius=.2,color=color.green)
                            s += posits[k,size-1-k,i]
                        if s == (size-2)*-2:
                            return (i,j,size-1-j)
                        if dtot[1] == (size-2)*-2:
                            return (i,j,size-1-j)
                    if j == size-1 and i == size-1:
                        s = 0
                        for k in range(size):
                            #sphere(pos=(size-1-k+SPACING+XOFFSET[k],i+SPACING,0),radius=.2,color=color.green)
                            s += posits[size-1-k,i,k]
                        if s == (size-2)*-2:
                            return (i,j,size-1-j)
                        s = 0
                        for k in range(size):
                            #sphere(pos=(k+SPACING+XOFFSET[size-1-i],k+SPACING,0),radius=.2,color=color.green)
                            s += posits[k,k,size-1-i]
                        if s == (size-2)*-2:
                            return (i,j,size-1-j)
                        if dtot[3] == (size-2)*-2:
                            return (i,j,size-1-j)

    for i in range(size):
        tot = [0,0]
        for j in range(size):
            tot[0] += posits[j,i,j]
            tot[1] += posits[j,i,size-1-j]
        if tot[0] == (size-2)*-2:
            #print "YAY!"
            for j in range(size):
                #pos = (j,i,j)
                if positions[(j,i,j)] == 0:
                    if sum(posits[j,i,:]) == (size-2)*-2 or sum(posits[j,:,j]) == (size-2)*-2 or sum(posits[:,i,j]) == (size-2)*-2:
                        return (j,i,j)
                    if j == 0 and i == 0:
                        s = 0
                        for k in range(size):
                            #sphere(pos=(k+SPACING+XOFFSET[i],k+SPACING,0),radius=.2,color=color.green)
                            s += posits[k,k,i]
                        if s == (size-2)*-2:
                            return (j,i,j)
                        s = 0
                        for k in range(size):
                            #sphere(pos=(i+SPACING+XOFFSET[k],k+SPACING,0),radius=.2,color=color.green)
                            s += posits[i,k,k]
                        if s == (size-2)*-2:
                            return (j,i,j)
                        if dtot[0] == (size-2)*-2:
                            return (j,i,j)
                    if j == 0 and i == size-1:
                        s = 0
                        for k in range(size):
                            #sphere(pos=(size-1-k+SPACING+XOFFSET[size-1-i],k+SPACING,0),radius=.2,color=color.green)
                            s += posits[size-1-k,k,size-1-i]
                        if s == (size-2)*-2:
                            return (j,i,j)
                        s = 0
                        for k in range(size):
                            #sphere(pos=(size-1-i+SPACING+XOFFSET[k],size-1-k+SPACING,0),radius=.2,color=color.green)
                            s += posits[size-1-i,size-1-k,k]
                        if s == (size-2)*-2:
                            return (j,i,j)
                        if dtot[1] == (size-2)*-2:
                            return (j,i,j)
                    if j == size-1 and i == 0:
                        s = 0
                        for k in range(size):
                            #sphere(pos=(size-1-k+SPACING+XOFFSET[size-1-i],k+SPACING,0),radius=.2,color=color.green)
                            s += posits[size-1-k,k,size-1-i]
                        if s == (size-2)*-2:
                            return (j,i,j)
                        s = 0
                        for k in range(size):
                            #sphere(pos=(size-1-i+SPACING+XOFFSET[k],size-1-k+SPACING,0),radius=.2,color=color.green)
                            s += posits[size-1-i,size-1-k,k]
                        if s == (size-2)*-2:
                            return (j,i,j)
                        if dtot[1] == (size-2)*-2:
                            return (j,i,j)
                    if j == size-1 and i == size-1:
                        s = 0
                        for k in range(size):
                            #sphere(pos=(k+SPACING+XOFFSET[i],k+SPACING,0),radius=.2,color=color.green)
                            s += posits[k,k,i]
                        if s == (size-2)*-2:
                            return (j,i,j)
                        s = 0
                        for k in range(size):
                            #sphere(pos=(i+SPACING+XOFFSET[k],k+SPACING,0),radius=.2,color=color.green)
                            s += posits[i,k,k]
                        if s == (size-2)*-2:
                            return (j,i,j)
                        if dtot[0] == (size-2)*-2:
                            return (j,i,j)
        if tot[1] == (size-2)*-2:
            for j in range(size):
                #pos = (j,i,size-1-j)
                if positions[(j,i,size-1-j)] == 0:
                    if sum(posits[j,i,:]) == (size-2)*-2 or sum(posits[j,:,size-1-j]) == (size-2)*-2 or sum(posits[:,i,size-1-j]) == (size-2)*-2:
                        return (j,i,size-1-j)
                    if j == 0 and i == 0:
                        s = 0
                        for k in range(size):
                            #sphere(pos=(k+SPACING+XOFFSET[size-1-i],k+SPACING,0),radius=.2,color=color.green)
                            s += posits[k,k,size-1-i]
                        if s == (size-2)*-2:
                            return (j,i,size-1-j)
                        s = 0
                        for k in range(size):
                            #sphere(pos=(i+SPACING+XOFFSET[k],size-1-k+SPACING,0),radius=.2,color=color.green)
                            s += posits[i,size-1-k,k]
                        if s == (size-2)*-2:
                            return (j,i,size-1-j)
                        if dtot[3] == (size-2)*-2:
                            return (j,i,size-1-j)
                    if j == 0 and i == size-1:
                        s = 0
                        for k in range(size):
                            #sphere(pos=(size-1-k+SPACING+XOFFSET[i],k+SPACING,0),radius=.2,color=color.green)
                            s += posits[size-1-k,k,i]
                        if s == (size-2)*-2:
                            return (j,i,size-1-j)
                        s = 0
                        for k in range(size):
                            #sphere(pos=(size-1-i+SPACING+XOFFSET[k],k+SPACING,0),radius=.2,color=color.green)
                            s += posits[size-1-i,k,k]
                        if s == (size-2)*-2:
                            return (j,i,size-1-j)
                        if dtot[2] == (size-2)*-2:
                            return (j,i,size-1-j)
                    if j == size-1 and i == 0:
                        s = 0
                        for k in range(size):
                            #sphere(pos=(size-1-k+SPACING+XOFFSET[i],k+SPACING,0),radius=.2,color=color.green)
                            s += posits[size-1-k,k,i]
                        if s == (size-2)*-2:
                            return (j,i,size-1-j)
                        s = 0
                        for k in range(size):
                            #sphere(pos=(size-1-i+SPACING+XOFFSET[k],k+SPACING,0),radius=.2,color=color.green)
                            s += posits[size-1-i,k,k]
                        if s == (size-2)*-2:
                            return (j,i,size-1-j)
                        if dtot[2] == (size-2)*-2:
                            return (j,i,size-1-j)
                    if j == size-1 and i == size-1:
                        s = 0
                        for k in range(size):
                            #sphere(pos=(k+SPACING+XOFFSET[size-1-i],k+SPACING,0),radius=.2,color=color.green)
                            s += posits[k,k,size-1-i]
                        if s == (size-2)*-2:
                            return (j,i,size-1-j)
                        s = 0
                        for k in range(size):
                            #sphere(pos=(i+SPACING+XOFFSET[k],size-1-k+SPACING,0),radius=.2,color=color.green)
                            s += posits[i,size-1-k,k]
                        if s == (size-2)*-2:
                            return (j,i,size-1-j)
                        if dtot[3] == (size-2)*-2:
                            return (j,i,size-1-j)
    for i in range(size):
        tot = [0,0]
        for j in range(size):
            tot[0] += posits[j,j,i]
            tot[1] += posits[j,size-1-j,i]
        if tot[0] == (size-2)*-2:
            for j in range(size):
                #pos = (j,j,i)
                if positions[(j,j,i)] == 0:
                    if sum(posits[j,j,:]) == (size-2)*-2 or sum(posits[j,:,i]) == (size-2)*-2 or sum(posits[:,j,i]) == (size-2)*-2:
                        return (j,j,i)
                    if j == 0 and i == 0:
                        s = 0
                        for k in range(size):
                            #sphere(pos=(i+SPACING+XOFFSET[k],k+SPACING,0),radius=.2,color=color.green)
                            s += posits[i,k,k]
                        if s == (size-2)*-2:
                            return (j,j,i)
                        s = 0
                        for k in range(size):
                            #sphere(pos=(k+SPACING+XOFFSET[k],i+SPACING,0),radius=.2,color=color.green)
                            s += posits[k,i,k]
                        if s == (size-2)*-2:
                            return (j,j,i)
                        if dtot[0] == (size-2)*-2:
                            return (j,j,i)
                    if j == 0 and i == size-1:
                        s = 0
                        for k in range(size):
                            #sphere(pos=(size-1-i+SPACING+XOFFSET[k],size-1-k+SPACING,0),radius=.2,color=color.green)
                            s += posits[size-1-i,size-1-k,k]
                        if s == (size-2)*-2:
                            return (j,j,i)
                        s = 0
                        for k in range(size):
                            #sphere(pos=(size-1-k+SPACING+XOFFSET[k],size-1-i+SPACING,0),radius=.2,color=color.green)
                            s += posits[size-1-k,size-1-i,k]
                        if s == (size-2)*-2:
                            return (j,j,i)
                        if dtot[3] == (size-2)*-2:
                            return (j,j,i)
                    if j == size-1 and i == 0:
                        s = 0
                        for k in range(size):
                            #sphere(pos=(size-1-i+SPACING+XOFFSET[k],size-1-k+SPACING,0),radius=.2,color=color.green)
                            s += posits[size-1-i,size-1-k,k]
                        if s == (size-2)*-2:
                            return (j,j,i)
                        s = 0
                        for k in range(size):
                            #sphere(pos=(size-1-k+SPACING+XOFFSET[k],size-1-i+SPACING,0),radius=.2,color=color.green)
                            s += posits[size-1-k,size-1-i,k]
                        if s == (size-2)*-2:
                            return (j,j,i)
                        if dtot[3] == (size-2)*-2:
                            return (j,j,i)
                    if j == size-1 and i == size-1:
                        s = 0
                        for k in range(size):
                            #sphere(pos=(i+SPACING+XOFFSET[k],k+SPACING,0),radius=.2,color=color.green)
                            s += posits[i,k,k]
                        if s == (size-2)*-2:
                            return (j,j,i)
                        s = 0
                        for k in range(size):
                            #sphere(pos=(k+SPACING+XOFFSET[k],i+SPACING,0),radius=.2,color=color.green)
                            s += posits[k,i,k]
                        if s == (size-2)*-2:
                            return (j,j,i)
                        if dtot[0] == (size-2)*-2:
                            return (j,j,i)
        if tot[1] == (size-2)*-2:
            for j in range(size):
                #pos = (j,size-1-j,i)
                if positions[(j,size-1-j,i)] == 0:
                    if sum(posits[j,size-1-j,:]) == (size-2)*-2 or sum(posits[j,:,i]) == (size-2)*-2 or sum(posits[:,size-1-j,j]) == (size-2)*-2:
                        return (j,size-1-j,i)
                    if j == 0 and i == 0:
                        s = 0
                        for k in range(size):
                            #sphere(pos=(i+SPACING+XOFFSET[k],size-1-k+SPACING,0),radius=.2,color=color.green)
                            s += posits[i,size-1-k,k]
                        if s == (size-2)*-2:
                            return (j,size-1-j,i)
                        s = 0
                        for k in range(size):
                            #sphere(pos=(k+SPACING+XOFFSET[k],size-1-i+SPACING,0),radius=.2,color=color.green)
                            s += posits[k,size-1-i,k]
                        if s == (size-2)*-2:
                            return (j,size-1-j,i)
                        if dtot[1] == (size-2)*-2:
                            return (j,size-1-j,i)
                    if j == 0 and i == size-1:
                        s = 0
                        for k in range(size):
                            #sphere(pos=(size-1-i+SPACING+XOFFSET[k],k+SPACING,0),radius=.2,color=color.green)
                            s += posits[size-1-i,k,k]
                        if s == (size-2)*-2:
                            return (j,size-1-j,i)
                        s = 0
                        for k in range(size):
                            #sphere(pos=(size-1-k+SPACING+XOFFSET[k],i+SPACING,0),radius=.2,color=color.green)
                            s += posits[size-1-k,i,k]
                        if s == (size-2)*-2:
                            return (j,size-1-j,i)
                        if dtot[2] == (size-2)*-2:
                            return (j,size-1-j,i)
                    if j == size-1 and i == 0:
                        s = 0
                        for k in range(size):
                            #sphere(pos=(size-1-i+SPACING+XOFFSET[k],k+SPACING,0),radius=.2,color=color.green)
                            s += posits[size-1-i,k,k]
                        if s == (size-2)*-2:
                            return (j,size-1-j,i)
                        s = 0
                        for k in range(size):
                            #sphere(pos=(size-1-k+SPACING+XOFFSET[k],i+SPACING,0),radius=.2,color=color.green)
                            s += posits[size-1-k,i,k]
                        if s == (size-2)*-2:
                            return (j,size-1-j,i)
                        if dtot[2] == (size-2)*-2:
                            return (j,size-1-j,i)
                    if j == size-1 and i == size-1:
                        s = 0
                        for k in range(size):
                            #sphere(pos=(i+SPACING+XOFFSET[k],size-1-k+SPACING,0),radius=.2,color=color.green)
                            s += posits[i,size-1-k,k]
                        if s == (size-2)*-2:
                            return (j,size-1-j,i)
                        s = 0
                        for k in range(size):
                            #sphere(pos=(k+SPACING+XOFFSET[k],size-1-i+SPACING,0),radius=.2,color=color.green)
                            s += posits[k,size-1-i,k]
                        if s == (size-2)*-2:
                            return (j,size-1-j,i)
                        if dtot[1] == (size-2)*-2:
                            return (j,size-1-j,i)
    return (-1,-1,-1)

#SIZE = 4
#SPACING = .5
#XOFFSET = arange(0, (SIZE+SPACING)*SIZE, SIZE+SPACING)

def blockfork(positions):
    size = len(positions[0])
    replace = where(positions==1)
    posits = copy(positions)
    posits[replace[0],replace[1],replace[2]] = 2
    ax0 = where(posits.sum(axis=0)==2*(size-2))
    ax1 = where(posits.sum(axis=1)==2*(size-2))
    # Check for "row" forks
    for i in range(len(ax0[0])):
        for j in range(len(ax1[0])):
            if ax0[1][i] == ax1[1][j]:
                if positions[ax1[0][j],ax0[0][i],ax0[1][i]] == 0:
                    return (ax1[0][j],ax0[0][i],ax0[1][i])
    ax2 = where(posits.sum(axis=2)==2*(size-2))
    for i in range(len(ax0[0])):
        for j in range(len(ax2[0])):
            if ax0[0][i] == ax2[1][j]:
                if positions[ax2[0][j],ax0[0][i],ax0[1][i]] == 0:
                    return (ax2[0][j],ax0[0][i],ax0[1][i])
    for i in range(len(ax1[0])):
        for j in range(len(ax2[0])):
            if ax1[0][i] == ax2[0][j]:
                if positions[ax2[0][j],ax2[1][j],ax1[1][i]] == 0:
                    return (ax2[0][j],ax2[1][j],ax1[1][i])
    # Check for 3D diagonal with anything else fork
    offsets = [[0,0],[0,size-1],[size-1,0],[size-1,size-1]]
    dtot = [0]*(2**(DIM-1))
    for i in range(len(dtot)):
        for j in range(size):
            dtot[i] += posits[abs(j-offsets[i][0]),abs(j-offsets[i][1]),j]
    for i in range(len(dtot)):
        if dtot[i] == (size-2)*2:
            for j in range(size):
                pos = (abs(j-offsets[i][0]),abs(j-offsets[i][1]),j)
                if posits[pos] == 0:
                # Check each intersecting row
                    if sum(posits[pos[0],pos[1],:]) == (size-2)*2 or sum(posits[pos[0],:,pos[2]]) == (size-2)*2 or sum(posits[:,pos[1],pos[2]]) == (size-2)*2:
                        return tuple(pos)
#                if pos[0] == 0 or pos[0] == size-1 or pos[1] == 0 or pos[1] == size-1:
#                 #Corner piece - must check plane diagonal too
#                    s = 0
#                    for k in range(size):
#                        s += posits[abs(pos[0]-offsets[i][0]),pos[1],k]
#                    if s == (size-2)*2:
#                        return tuple(pos)
#                    s = 0
#                    for k in range(size):
#                        s += posits[pos[0],abs(pos[1]-offsets[i][0]),k]
#                    if s == (size-2)*2:
#                        return tuple(pos)

    for i in range(size):
        tot = [0,0]
        for j in range(size):
            tot[0] += posits[i,j,j]
            tot[1] += posits[i,j,size-1-j]
        if tot[0] == (size-2)*2:
            #print "Yay!"
            for j in range(size):
                if positions[(i,j,j)] == 0:
                    if sum(posits[i,j,:]) == (size-2)*2 or sum(posits[i,:,j]) == (size-2)*2 or sum(posits[:,j,j]) == (size-2)*2:
                        return (i,j,j)
                    if j == 0 and i == 0:
                        s = 0
                        for k in range(size):
                            #sphere(pos=(k+SPACING+XOFFSET[k],i+SPACING,0),radius=.2,color=color.green)
                            s += posits[k,i,k]
                        if s == (size-2)*2:
                            return (i,j,j)
                        s = 0
                        for k in range(size):
                            #sphere(pos=(k+SPACING+XOFFSET[i],k+SPACING,0),radius=.2,color=color.green)
                            s += posits[k,k,i]
                        if s == (size-2)*2:
                            return (i,j,j)
                        if dtot[0] == (size-2)*2:
                            return (i,j,j)
                    if j == 0 and i == size-1:
                        s = 0
                        for k in range(size):
                            #sphere(pos=(size-1-k+SPACING+XOFFSET[k],size-1-i+SPACING,0),radius=.2,color=color.green)
                            s += posits[size-1-k,size-1-i,k]
                        if s == (size-2)*2:
                            return (i,j,j)
                        s = 0
                        for k in range(size):
                            #sphere(pos=(k+SPACING+XOFFSET[size-1-i],size-1-k+SPACING,0),radius=.2,color=color.green)
                            s += posits[k,size-1-k,size-1-i]
                        if s == (size-2)*2:
                            return (i,j,j)
                        if dtot[2] == (size-2)*2:
                            return (i,j,j)
                    if j == size-1 and i == 0:
                        #print (i, j, j)
                        s = 0
                        for k in range(size):
                            #sphere(pos=(size-1-k+SPACING+XOFFSET[k],size-1-i+SPACING,0),radius=.2,color=color.green)
                            s += posits[size-1-k,size-1-i,k]
                        if s == (size-2)*2:
                            return (i,j,j)
                        s = 0
                        for k in range(size):
                            #sphere(pos=(size-1-k+SPACING+XOFFSET[size-1-i],k+SPACING,0),radius=.2,color=color.green)
                            s += posits[size-1-k,k,size-1-i]
                        if s == (size-2)*2:
                            return (i,j,j)
                        if dtot[2] == (size-2)*2:
                            return (i,j,j)
                    if j == size-1 and i == size-1:
                        s = 0
                        for k in range(size):
                            #sphere(pos=(k+SPACING+XOFFSET[k],i+SPACING,0),radius=.2,color=color.green)
                            s += posits[k,i,k]
                        if s == (size-2)*2:
                            return (i,j,j)
                        s = 0
                        for k in range(size):
                            #sphere(pos=(k+SPACING+XOFFSET[i],k+SPACING,0),radius=.2,color=color.green)
                            s += posits[k,k,i]
                        if s == (size-2)*2:
                            return (i,j,j)
                        if dtot[0] == (size-2)*2:
                            return (i,j,j)
        if tot[1] == (size-2)*2:
            #print "yay!"
            for j in range(size):
                if positions[(i,j,size-1-j)] == 0:
                    if sum(posits[i,j,:]) == (size-2)*2 or sum(posits[i,:,size-1-j]) == (size-2)*2 or sum(posits[:,j,size-1-j]) == (size-2)*2:
                        return (i,j,size-1-j)
                    if j == 0 and i == 0:
                        s = 0
                        for k in range(size):
                            #sphere(pos=(size-1-k+SPACING+XOFFSET[k],i+SPACING,0),radius=.2,color=color.green)
                            s += posits[size-1-k,i,k]
                        if s == (size-2)*2:
                            return (i,j,size-1-j)
                        s = 0
                        for k in range(size):
                            #sphere(pos=(k+SPACING+XOFFSET[size-1-i],k+SPACING,0),radius=.2,color=color.green)
                            s += posits[k,k,size-1-i]
                        if s == (size-2)*2:
                            return (i,j,size-1-j)
                        if dtot[3] == (size-2)*2:
                            return (i,j,size-1-j)
                    if j == 0 and i == size-1:
                        s = 0
                        for k in range(size):
                            #sphere(pos=(k+SPACING+XOFFSET[k],size-1-i+SPACING,0),radius=.2,color=color.green)
                            s += posits[k,size-1-i,k]
                        if s == (size-2)*2:
                            return (i,j,size-1-j)
                        s = 0
                        for k in range(size):
                            #sphere(pos=(size-1-k+SPACING+XOFFSET[i],k+SPACING,0),radius=.2,color=color.green)
                            s += posits[size-1-k,k,i]
                        if s == (size-2)*2:
                            return (i,j,size-1-j)
                        if dtot[1] == (size-2)*2:
                            return (i,j,size-1-j)
                    if j == size-1 and i == 0:
                        s = 0
                        for k in range(size):
                            #sphere(pos=(k+SPACING+XOFFSET[k],size-1-i+SPACING,0),radius=.2,color=color.green)
                            s += posits[k,size-1-i,k]
                        if s == (size-2)*2:
                            return (i,j,size-1-j)
                        s = 0
                        for k in range(size):
                            #sphere(pos=(k+SPACING+XOFFSET[i],size-1-k+SPACING,0),radius=.2,color=color.green)
                            s += posits[k,size-1-k,i]
                        if s == (size-2)*2:
                            return (i,j,size-1-j)
                        if dtot[1] == (size-2)*2:
                            return (i,j,size-1-j)
                    if j == size-1 and i == size-1:
                        s = 0
                        for k in range(size):
                            #sphere(pos=(size-1-k+SPACING+XOFFSET[k],i+SPACING,0),radius=.2,color=color.green)
                            s += posits[size-1-k,i,k]
                        if s == (size-2)*2:
                            return (i,j,size-1-j)
                        s = 0
                        for k in range(size):
                            #sphere(pos=(k+SPACING+XOFFSET[size-1-i],k+SPACING,0),radius=.2,color=color.green)
                            s += posits[k,k,size-1-i]
                        if s == (size-2)*2:
                            return (i,j,size-1-j)
                        if dtot[3] == (size-2)*2:
                            return (i,j,size-1-j)

    for i in range(size):
        tot = [0,0]
        for j in range(size):
            tot[0] += posits[j,i,j]
            tot[1] += posits[j,i,size-1-j]
        if tot[0] == (size-2)*2:
            #print "YAY!"
            for j in range(size):
                #pos = (j,i,j)
                if positions[(j,i,j)] == 0:
                    if sum(posits[j,i,:]) == (size-2)*2 or sum(posits[j,:,j]) == (size-2)*2 or sum(posits[:,i,j]) == (size-2)*2:
                        return (j,i,j)
                    if j == 0 and i == 0:
                        s = 0
                        for k in range(size):
                            #sphere(pos=(k+SPACING+XOFFSET[i],k+SPACING,0),radius=.2,color=color.green)
                            s += posits[k,k,i]
                        if s == (size-2)*2:
                            return (j,i,j)
                        s = 0
                        for k in range(size):
                            #sphere(pos=(i+SPACING+XOFFSET[k],k+SPACING,0),radius=.2,color=color.green)
                            s += posits[i,k,k]
                        if s == (size-2)*2:
                            return (j,i,j)
                        if dtot[0] == (size-2)*2:
                            return (j,i,j)
                    if j == 0 and i == size-1:
                        s = 0
                        for k in range(size):
                            #sphere(pos=(size-1-k+SPACING+XOFFSET[size-1-i],k+SPACING,0),radius=.2,color=color.green)
                            s += posits[size-1-k,k,size-1-i]
                        if s == (size-2)*2:
                            return (j,i,j)
                        s = 0
                        for k in range(size):
                            #sphere(pos=(size-1-i+SPACING+XOFFSET[k],size-1-k+SPACING,0),radius=.2,color=color.green)
                            s += posits[size-1-i,size-1-k,k]
                        if s == (size-2)*2:
                            return (j,i,j)
                        if dtot[1] == (size-2)*2:
                            return (j,i,j)
                    if j == size-1 and i == 0:
                        s = 0
                        for k in range(size):
                            #sphere(pos=(size-1-k+SPACING+XOFFSET[size-1-i],k+SPACING,0),radius=.2,color=color.green)
                            s += posits[size-1-k,k,size-1-i]
                        if s == (size-2)*2:
                            return (j,i,j)
                        s = 0
                        for k in range(size):
                            #sphere(pos=(size-1-i+SPACING+XOFFSET[k],size-1-k+SPACING,0),radius=.2,color=color.green)
                            s += posits[size-1-i,size-1-k,k]
                        if s == (size-2)*2:
                            return (j,i,j)
                        if dtot[1] == (size-2)*2:
                            return (j,i,j)
                    if j == size-1 and i == size-1:
                        s = 0
                        for k in range(size):
                            #sphere(pos=(k+SPACING+XOFFSET[i],k+SPACING,0),radius=.2,color=color.green)
                            s += posits[k,k,i]
                        if s == (size-2)*2:
                            return (j,i,j)
                        s = 0
                        for k in range(size):
                            #sphere(pos=(i+SPACING+XOFFSET[k],k+SPACING,0),radius=.2,color=color.green)
                            s += posits[i,k,k]
                        if s == (size-2)*2:
                            return (j,i,j)
                        if dtot[0] == (size-2)*2:
                            return (j,i,j)
        if tot[1] == (size-2)*2:
            for j in range(size):
                #pos = (j,i,size-1-j)
                if positions[(j,i,size-1-j)] == 0:
                    if sum(posits[j,i,:]) == (size-2)*2 or sum(posits[j,:,size-1-j]) == (size-2)*2 or sum(posits[:,i,size-1-j]) == (size-2)*2:
                        return (j,i,size-1-j)
                    if j == 0 and i == 0:
                        s = 0
                        for k in range(size):
                            #sphere(pos=(k+SPACING+XOFFSET[size-1-i],k+SPACING,0),radius=.2,color=color.green)
                            s += posits[k,k,size-1-i]
                        if s == (size-2)*2:
                            return (j,i,size-1-j)
                        s = 0
                        for k in range(size):
                            #sphere(pos=(i+SPACING+XOFFSET[k],size-1-k+SPACING,0),radius=.2,color=color.green)
                            s += posits[i,size-1-k,k]
                        if s == (size-2)*2:
                            return (j,i,size-1-j)
                        if dtot[3] == (size-2)*2:
                            return (j,i,size-1-j)
                    if j == 0 and i == size-1:
                        s = 0
                        for k in range(size):
                            #sphere(pos=(size-1-k+SPACING+XOFFSET[i],k+SPACING,0),radius=.2,color=color.green)
                            s += posits[size-1-k,k,i]
                        if s == (size-2)*2:
                            return (j,i,size-1-j)
                        s = 0
                        for k in range(size):
                            #sphere(pos=(size-1-i+SPACING+XOFFSET[k],k+SPACING,0),radius=.2,color=color.green)
                            s += posits[size-1-i,k,k]
                        if s == (size-2)*2:
                            return (j,i,size-1-j)
                        if dtot[2] == (size-2)*2:
                            return (j,i,size-1-j)
                    if j == size-1 and i == 0:
                        s = 0
                        for k in range(size):
                            #sphere(pos=(size-1-k+SPACING+XOFFSET[i],k+SPACING,0),radius=.2,color=color.green)
                            s += posits[size-1-k,k,i]
                        if s == (size-2)*2:
                            return (j,i,size-1-j)
                        s = 0
                        for k in range(size):
                            #sphere(pos=(size-1-i+SPACING+XOFFSET[k],k+SPACING,0),radius=.2,color=color.green)
                            s += posits[size-1-i,k,k]
                        if s == (size-2)*2:
                            return (j,i,size-1-j)
                        if dtot[2] == (size-2)*2:
                            return (j,i,size-1-j)
                    if j == size-1 and i == size-1:
                        s = 0
                        for k in range(size):
                            #sphere(pos=(k+SPACING+XOFFSET[size-1-i],k+SPACING,0),radius=.2,color=color.green)
                            s += posits[k,k,size-1-i]
                        if s == (size-2)*2:
                            return (j,i,size-1-j)
                        s = 0
                        for k in range(size):
                            #sphere(pos=(i+SPACING+XOFFSET[k],size-1-k+SPACING,0),radius=.2,color=color.green)
                            s += posits[i,size-1-k,k]
                        if s == (size-2)*2:
                            return (j,i,size-1-j)
                        if dtot[3] == (size-2)*2:
                            return (j,i,size-1-j)
    for i in range(size):
        tot = [0,0]
        for j in range(size):
            tot[0] += posits[j,j,i]
            tot[1] += posits[j,size-1-j,i]
        if tot[0] == (size-2)*2:
            for j in range(size):
                #pos = (j,j,i)
                if positions[(j,j,i)] == 0:
                    if sum(posits[j,j,:]) == (size-2)*2 or sum(posits[j,:,i]) == (size-2)*2 or sum(posits[:,j,i]) == (size-2)*2:
                        return (j,j,i)
                    if j == 0 and i == 0:
                        s = 0
                        for k in range(size):
                            #sphere(pos=(i+SPACING+XOFFSET[k],k+SPACING,0),radius=.2,color=color.green)
                            s += posits[i,k,k]
                        if s == (size-2)*2:
                            return (j,j,i)
                        s = 0
                        for k in range(size):
                            #sphere(pos=(k+SPACING+XOFFSET[k],i+SPACING,0),radius=.2,color=color.green)
                            s += posits[k,i,k]
                        if s == (size-2)*2:
                            return (j,j,i)
                        if dtot[0] == (size-2)*2:
                            return (j,j,i)
                    if j == 0 and i == size-1:
                        s = 0
                        for k in range(size):
                            #sphere(pos=(size-1-i+SPACING+XOFFSET[k],size-1-k+SPACING,0),radius=.2,color=color.green)
                            s += posits[size-1-i,size-1-k,k]
                        if s == (size-2)*2:
                            return (j,j,i)
                        s = 0
                        for k in range(size):
                            #sphere(pos=(size-1-k+SPACING+XOFFSET[k],size-1-i+SPACING,0),radius=.2,color=color.green)
                            s += posits[size-1-k,size-1-i,k]
                        if s == (size-2)*2:
                            return (j,j,i)
                        if dtot[3] == (size-2)*2:
                            return (j,j,i)
                    if j == size-1 and i == 0:
                        s = 0
                        for k in range(size):
                            #sphere(pos=(size-1-i+SPACING+XOFFSET[k],size-1-k+SPACING,0),radius=.2,color=color.green)
                            s += posits[size-1-i,size-1-k,k]
                        if s == (size-2)*2:
                            return (j,j,i)
                        s = 0
                        for k in range(size):
                            #sphere(pos=(size-1-k+SPACING+XOFFSET[k],size-1-i+SPACING,0),radius=.2,color=color.green)
                            s += posits[size-1-k,size-1-i,k]
                        if s == (size-2)*2:
                            return (j,j,i)
                        if dtot[3] == (size-2)*2:
                            return (j,j,i)
                    if j == size-1 and i == size-1:
                        s = 0
                        for k in range(size):
                            #sphere(pos=(i+SPACING+XOFFSET[k],k+SPACING,0),radius=.2,color=color.green)
                            s += posits[i,k,k]
                        if s == (size-2)*2:
                            return (j,j,i)
                        s = 0
                        for k in range(size):
                            #sphere(pos=(k+SPACING+XOFFSET[k],i+SPACING,0),radius=.2,color=color.green)
                            s += posits[k,i,k]
                        if s == (size-2)*2:
                            return (j,j,i)
                        if dtot[0] == (size-2)*2:
                            return (j,j,i)
        if tot[1] == (size-2)*2:
            for j in range(size):
                #pos = (j,size-1-j,i)
                if positions[(j,size-1-j,i)] == 0:
                    if sum(posits[j,size-1-j,:]) == (size-2)*2 or sum(posits[j,:,i]) == (size-2)*2 or sum(posits[:,size-1-j,j]) == (size-2)*2:
                        return (j,size-1-j,i)
                    if j == 0 and i == 0:
                        s = 0
                        for k in range(size):
                            #sphere(pos=(i+SPACING+XOFFSET[k],size-1-k+SPACING,0),radius=.2,color=color.green)
                            s += posits[i,size-1-k,k]
                        if s == (size-2)*2:
                            return (j,size-1-j,i)
                        s = 0
                        for k in range(size):
                            #sphere(pos=(k+SPACING+XOFFSET[k],size-1-i+SPACING,0),radius=.2,color=color.green)
                            s += posits[k,size-1-i,k]
                        if s == (size-2)*2:
                            return (j,size-1-j,i)
                        if dtot[1] == (size-2)*2:
                            return (j,size-1-j,i)
                    if j == 0 and i == size-1:
                        s = 0
                        for k in range(size):
                            #sphere(pos=(size-1-i+SPACING+XOFFSET[k],k+SPACING,0),radius=.2,color=color.green)
                            s += posits[size-1-i,k,k]
                        if s == (size-2)*2:
                            return (j,size-1-j,i)
                        s = 0
                        for k in range(size):
                            #sphere(pos=(size-1-k+SPACING+XOFFSET[k],i+SPACING,0),radius=.2,color=color.green)
                            s += posits[size-1-k,i,k]
                        if s == (size-2)*2:
                            return (j,size-1-j,i)
                        if dtot[2] == (size-2)*2:
                            return (j,size-1-j,i)
                    if j == size-1 and i == 0:
                        s = 0
                        for k in range(size):
                            #sphere(pos=(size-1-i+SPACING+XOFFSET[k],k+SPACING,0),radius=.2,color=color.green)
                            s += posits[size-1-i,k,k]
                        if s == (size-2)*2:
                            return (j,size-1-j,i)
                        s = 0
                        for k in range(size):
                            #sphere(pos=(size-1-k+SPACING+XOFFSET[k],i+SPACING,0),radius=.2,color=color.green)
                            s += posits[size-1-k,i,k]
                        if s == (size-2)*2:
                            return (j,size-1-j,i)
                        if dtot[2] == (size-2)*2:
                            return (j,size-1-j,i)
                    if j == size-1 and i == size-1:
                        s = 0
                        for k in range(size):
                            #sphere(pos=(i+SPACING+XOFFSET[k],size-1-k+SPACING,0),radius=.2,color=color.green)
                            s += posits[i,size-1-k,k]
                        if s == (size-2)*2:
                            return (j,size-1-j,i)
                        s = 0
                        for k in range(size):
                            #sphere(pos=(k+SPACING+XOFFSET[k],size-1-i+SPACING,0),radius=.2,color=color.green)
                            s += posits[k,size-1-i,k]
                        if s == (size-2)*2:
                            return (j,size-1-j,i)
                        if dtot[1] == (size-2)*2:
                            return (j,size-1-j,i)
    return (-1,-1,-1)

def move(positions):
    if sum(abs(positions.flatten())) == 0:
        return (1,1,1)
    pos, move = canwin(positions)
    if move:
        return pos
    pos, move = oppwin(positions)
    if move:
        return pos
    pos = createfork(positions)
    if sum(pos) >= 0:
        return pos
    pos = blockfork(positions)
    if sum(pos) >= 0:
        return pos
    #return randmove(positions)
