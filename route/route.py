#!/usr/bin/env python

import math
import random
import numpy


# Define a routing grid
# Origin 0, 0 is in lower-left corner
class rgrid:
    def __init__(self, x=10, y=10):
        self.x_dim = x
        self.y_dim = y
        self.grid = numpy.array([[0] * x for yp in range(y)])

    def display(self):
        for y in range(self.y_dim-1, -1, -1):
            line = ''
            for x in range(self.x_dim):
                if self.grid[x][y] == 0:
                    line += '.'
                else:
                    line += '*'
            print line

    def op_or(self, rg):
        if rg.x_dim != self.x_dim or rg.y_dim != self.y_dim:
            return None
        rv = rgrid(self.x_dim, self.y_dim)
        rv.grid = self.grid or rg.grid
        return rv

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
            fval.append(math.pow(math.e, -temp))

        out = []
        for o in range(self.outputs):
            temp = 0.0
            for f in range(self.func):
                temp += self.weight[o][f] * fval[f]
            out.append(temp)
        return out


class router:
    def __init__(self, rg=None):
        self.grid = rg
        self.cur = (0, 0)
        self.target = (0, 0)
        self.rbf = rbfnet(6, 4, 4)
        self.rbf.randomize()

    def set_position(self, x, y):
        self.cur = (x, y)

    def set_target(self, x, y):
        self.target = (x, y)

    def manhattan(self):
        return abs(self.target[0]-self.cur[0])+abs(self.target[1]-self.cur[1])

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
        if not bvec[0] and self.cur[0] > 0 and self.grid.grid[self.cur[0]-1][self.cur[1]] != 0:
            bvec[0] = True
        elif not bvec[2] and self.cur[0] < (self.grid.x_dim-1) and self.grid.grid[self.cur[0]+1][self.cur[1]] != 0:
            bvec[2] = True
        if not bvec[1] and self.cur[1] < (self.grid.y_dim-1) and self.grid.grid[self.cur[0]][self.cur[1]+1] != 0:
            bvec[1] = True
        elif not bvec[3] and self.cur[1] > 0 and self.grid.grid[self.cur[0]][self.cur[1]-1] != 0:
            bvec[3] = True

        # Set blocked if grid is used 1 space away
        if not bvec[0] and self.cur[0] > 1 and self.grid.grid[self.cur[0]-2][self.cur[1]] != 0:
            bvec[0] = True
        elif not bvec[2] and self.cur[0] < (self.grid.x_dim-2) and self.grid.grid[self.cur[0]+2][self.cur[1]] != 0:
            bvec[2] = True
        if not bvec[1] and self.cur[1] < (self.grid.y_dim-2) and self.grid.grid[self.cur[0]][self.cur[1]+2] != 0:
            bvec[1] = True
        elif not bvec[3] and self.cur[1] > 1 and self.grid.grid[self.cur[0]][self.cur[1]-2] != 0:
            bvec[3] = True


        # # Set blocked if grid is used 2 space away
        # # Need edge of grid check
        # if not bvec[0] and self.grid.grid[self.cur[0]-2][self.cur[1]] != 0:
        #     bvec[0] = True
        # if not bvec[1] and self.grid.grid[self.cur[0]][self.cur[1]+2] != 0:
        #     bvec[1] = True
        # if not bvec[2] and self.grid.grid[self.cur[0]+2][self.cur[1]] != 0:
        #     bvec[2] = True
        # if not bvec[3] and self.grid.grid[self.cur[0]][self.cur[1]-2] != 0:
        #     bvec[3] = True

        return bvec

    def mark(self):
        self.grid.grid[self.cur[0]][self.cur[1]] = 1

    # move in a direction, directions are 0=West,1=North,2=East,3=South
    def move(self, dir=0):
        bvec = self.blocked()
        if bvec[dir]:
            return
        else:
            print "Debug: cur",self.cur,"move",dir,"blocked",bvec
            if dir == 0:
                self.cur = (self.cur[0]-1, self.cur[1])
            elif dir == 1:
                self.cur = (self.cur[0], self.cur[1]+1)
            elif dir == 2:
                self.cur = (self.cur[0]+1, self.cur[1])
            elif dir == 3:
                self.cur = (self.cur[0], self.cur[1]-1)
            self.mark()

    def do_route(self):
        # normalize x delta
        delta_x = ((self.target[0]-self.cur[0])/float(self.grid.x_dim)/2.0+0.5)
        delta_y = ((self.target[1]-self.cur[1])/float(self.grid.y_dim)/2.0+0.5)
        trials = self.manhattan()*3
        print "Manhattan distance", self.manhattan()
        self.mark()
        while trials > 0 and self.target != self.cur:
            inputs = [delta_x, delta_y]+self.blocked()
            result = self.rbf.eval(inputs)
            movedir = numpy.argmax(result)
            print "Trials", trials, "result", result, "movedir=", movedir
            self.move(movedir)
            trials -= 1

    def score(self):
        s = 0
        if self.cur == self.target:
            s += 100
        else:
            s += 20 - self.manhattan()
        return s


def training_loop():
    max_score = 0
    best_rbf = None

    for t in range(1000):
        rg = rgrid()
        rg.grid[0][3] = 2

        r = router(rg)
        r.target = (7, 7)
        r.do_route()
        r.grid.display()

        if r.score() > max_score:
            print "Updating new best score", r.score()
            best_rbf = r.rbf
            max_score = r.score()

    rg = rgrid()
    rg.grid[0][3] = 2
    r = router(rg)
    r.rbf = best_rbf
    r.target = (7, 7)
    r.do_route()
    r.grid.display()

training_loop()
