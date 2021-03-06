from numpy import *

positions = array([[ 1.,  0.,  0.],
       [ 0., -1.,  0.],
       [ 0.,  0.,  1.]])

poslist = []
# Rows
for i in range(2):
    ax = where(positions.sum(axis=i)==-1)[0]
    if len(ax) > 0:
        for j in ax:
            pos1, pos2 = [0,0], [0,0]
            pos1[2-1-i], pos2[2-1-i] = j, j
            pos1[i] = where(take(positions,[j],axis=2-1-i).flatten()==0)[0][0]
            pos2[i] = where(take(positions,[j],axis=2-1-i).flatten()==0)[0][1]
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
print positions
print poslist
