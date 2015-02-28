#!/usr/bin/env python

import numpy
import unittest
import random
import math


# class for creating RBF neural network
class rbfnet:
    def __init__(self, dim=2, func=2, outputs=2):
        self.dim = dim
        self.func = func
        self.outputs = outputs
        self.center = numpy.array([[0.0] * dim for f in range(func)])
        self.weight = numpy.array([[0.0] * func for o in range(outputs)])

    def to_genotype(self):
        return numpy.concatenate([self.center.flatten(), self.weight.flatten()])

    def from_genotype(self, gene):
        c = numpy.array(gene[0:self.dim*self.func])
        w = numpy.array(gene[self.dim*self.func:])
        self.center = c.reshape(self.dim, self.func)
        self.weight = w.reshape(self.func, self.outputs)

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


class Testbench(unittest.TestCase):
    def setUp(self):
        pass

    def test_recode(self):
        for dim in range(2, 6):
            for func in range(2, 6):
                for outputs in range(2, 6):
                    r = rbfnet(dim, func, outputs)
                    r.randomize()
                    g = r.to_genotype()
                    print repr(g)
                    r2 = rbfnet(dim, func, outputs)
                    r2.from_genotype(g)

                    self.assertEqual(r2.to_genotype().sum() - g.sum(), 0.0)


if __name__ == "__main__":
    unittest.main()
