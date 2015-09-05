from numpy import *

DIM = 2

# Returns a random open position on the board
def randmove(positions):
    free = []
    for i in range(3):
        for j in range(3):
            if positions[i,j] == 0:
                free.append((i,j))
    return free[random.randint(len(free))]

def canwin(positions):
    pos = [-1, -1]
    for i in range(DIM):
        axwin = where(positions.sum(axis=i)==-2)[0]
        if len(axwin) > 0:
            pos[DIM-1-i] = axwin[0]
            pos[i] = where(take(positions,[axwin[0]],axis=DIM-1-i).flatten()==0)[0][0]
            return tuple(pos), True
    if trace(positions) == -2:
        i = where(positions.diagonal()==0)[0][0]
        return (i,i), True
    posrot = rot90(positions)
    if trace(posrot) == -2:
        i = where(posrot.diagonal()==0)[0][0]
        return (i,2-i), True
    return tuple(pos), False

def oppwin(positions):
    pos = [-1, -1]
    for i in range(DIM):
        axwin = where(positions.sum(axis=i)==2)[0]
        if len(axwin) > 0:
            pos[DIM-1-i] = axwin[0]
            pos[i] = where(take(positions,[axwin[0]],axis=DIM-1-i).flatten()==0)[0][0]
            return tuple(pos), True
    if trace(positions) == 2:
        i = where(positions.diagonal()==0)[0][0]
        return (i,i), True
    posrot = rot90(positions)
    if trace(posrot) == 2:
        i = where(posrot.diagonal()==0)[0][0]
        return (i,len(positions[0])-1-i), True
    return tuple(pos), False

def createfork(positions):
    axes = []
    for i in range(DIM):
        axes.append(where(positions.sum(axis=i)==-1)[0])
    if len(axes) == 2:
        for i in axes[0]:
            for j in axes[1]:
                if positions[j,i] != -1 and positions[j,i] == 0:
                    return (j,i), True
    return (-1,-1), False

# Returns a list of moves that would force opponent to defend by creating two in a row
def forcedefend(positions):
    poslist = []
    # Rows
    for i in range(DIM):
        ax = where(positions.sum(axis=i)==-1)[0]
        if len(ax) > 0:
            for j in ax:
                icoord = where(take(positions,[j],axis=DIM-1-i).flatten()==0)[0]
                if len(icoord) == 2:
                    pos1, pos2 = [0,0], [0,0]
                    pos1[DIM-1-i], pos2[DIM-1-i] = j, j
                    pos1[i] = icoord[0]
                    pos2[i] = icoord[1]
                    poslist.append([tuple(pos1),tuple(pos2)])
    # Diagonals
    if trace(positions) == -1:
        i = where(positions.diagonal()==0)[0]
        if len(i) == 2:
            poslist.append([(i[0],i[0]),(i[1],i[1])])
    posrot = rot90(positions)
    if trace(posrot) == -1:
        i = where(posrot.diagonal()==0)[0]
        if len(i) == 2:
            poslist.append([(i[0],2-i[0]),(i[1],2-i[1])])
    return poslist

def blockfork(positions):
    axes = []
    for i in range(DIM):
        axes.append(where(positions.sum(axis=i)==1)[0])
    if len(axes) == 2:
        forks = []
        for i in axes[0]:
            for j in axes[1]:
                if positions[j,i] != 1:
                    forks.append((j,i))
        if len(forks) > 0:
            poslist = forcedefend(positions)
            for pair in poslist:
                good = True
                for p in forks:
                    if pair[0] == p:
                        good = False
                if good:
                    return pair[1], True
                good = True
                for p in forks:
                    if pair[1] == p:
                        good = False
                if good:
                    return pair[1], True
    return (-1,-1), False

def move(positions):
    # Win if possible
    pos, move = canwin(positions)
    if move:
        #print "Win"
        return pos
    # Block opponent from winning 
    pos, move = oppwin(positions)
    if move:
        #print "Block win"
        return pos
    # Create a fork
    pos, move = createfork(positions)
    if move:
        #print "Creating a fork"
        return pos
    # Block a fork
    pos, move = blockfork(positions)
    if move:
        #print "Blocking a fork"
        return pos
    # If board is empty, play corner
    if len(where(positions.flatten()==0)[0]) == 9:
        #print "Play corner, first move"
        return (0,0)
    # Play center
    if positions[1,1] == 0:
        #print "Play center"
        return (1,1)
    # Play opposite corner of opponent
    for i in [0,2]:
        for j in [0,2]:
            if positions[i,j] == 1 and positions[i^2,j^2] == 0:
                #print "Play opposite corner of opponent"
                return (i^2,j^2)
        # Play opposite corner of self
    for i in [0,2]:
        for j in [0,2]:
            if positions[i,j] == -1 and positions[i^2,j^2] == 0:
                #print "Play opposite corner of self"
                return (i^2,j^2)
    # Play random empty corner, otherwise play random side
    corners = []
    for i in [0,2]:
        for j in [0,2]:
            if positions[i,j] == 0:
                corners.append((i,j))
    #print "Play random"
    return corners[random.randint(len(corners))] if len(corners) > 0 else randmove(positions)
