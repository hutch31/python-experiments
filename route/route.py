#!/usr/bin/env python

import math, random

# Define a routing grid
# Origin 0, 0 is in lower-left corner
class rgrid:
    def __init__(self, x=10, y=10):
        self.x_dim = x
        self.y_dim = y
        self.grid  = [[0] * x for yp in range(y)]

    def display (self):
        for y in range(self.y_dim):
            line = ''
            for x in range(self.x_dim):
                if self.grid[x][y] == 0:
                    line += '.'
                else:
                    line += '*'
            print line

class rbfnet:
    def __init__(self, dim=2, func=2, outputs=2):
        self.dim = dim
        self.func = func
        self.outputs = outputs
        self.center = [[0.0] * dim for f in range(func)]
        self.weight = [[0.0] * func for o in range(outputs)]

    def randomize(self):
        for f in range(self.func):
            for d in range(self.dim):
                self.center[f][d] = random.random()
        for o in range(self.outputs):
            for f in range(self.func):
                self.weight[o][f] = random.random()

    def eval(self, inputs):
        if len(inputs) != self.dim:
            raise ValueError('# Inputs must match RBF dimension')

        fval = []
        for ci in range(self.func):
            temp = 0.0
            for cj in range(self.dim):
                temp += math.pow(self.center[ci][cj] - inputs[cj], 2)
            fval.append (math.pow(math.e, -temp))

        out = []
        for o in range(self.outputs):
            temp = 0.0
            for f in range(self.func):
                temp += self.weight[o][f] * fval[f]
            out.append (temp)
        return out



class router:
    def __init__(self, rg=None):
        self.grid = rg
        self.cur = (0, 0)
        self.target = (0, 0)

    def set_position(self, x, y):
        self.cur = (x, y)

    def set_target(self, x, y):
        self.target = (x, y)

    # determine if path is blocked in any of 4 directions
    # returns [West, North, East, South]
    def blocked(self):
        bvec = [False]*4

        # Set blocked if we are on an edge
        if (self.cur[0] == 0):
            bvec[0] = True
        elif (self.cur[0] == (self.grid.x_dim-1)):
            bvec[2] = True
        if (self.cur[1] == 0):
            bvec[3] = True
        elif (self.cur[1] == (self.grid.y_dim-1)):
            bvec[1] = True

        # Set blocked if grid is used 1 space away
        if not bvec[0] and self.grid.grid[self.cur[0]-1][self.cur[1]] != 0:
            bvec[0] = True
        if not bvec[1] and self.grid.grid[self.cur[0]][self.cur[1]+1] != 0:
            bvec[1] = True
        if not bvec[2] and self.grid.grid[self.cur[0]+1][self.cur[1]] != 0:
            bvec[2] = True
        if not bvec[3] and self.grid.grid[self.cur[0]][self.cur[1]-1] != 0:
            bvec[3] = True

        # Set blocked if grid is used 2 space away
        # Need edge of grid check
        if not bvec[0] and self.grid.grid[self.cur[0]-2][self.cur[1]] != 0:
            bvec[0] = True
        if not bvec[1] and self.grid.grid[self.cur[0]][self.cur[1]+2] != 0:
            bvec[1] = True
        if not bvec[2] and self.grid.grid[self.cur[0]+2][self.cur[1]] != 0:
            bvec[2] = True
        if not bvec[3] and self.grid.grid[self.cur[0]][self.cur[1]-2] != 0:
            bvec[3] = True

        return bvec

rg = rgrid()
rg.display()

r = router(rg)
print r.blocked()

# create rbf network
rbf = rbfnet(2, 3, 4)
rbf.randomize()
print rbf.eval ([0.0,0.0])
