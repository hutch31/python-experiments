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

    def geno_size(self):
        return self.dim*self.func + self.func*self.range

    def to_gene(self):
        return numpy.concatenate([self.center.flatten(), self.weight.flatten()])

    def from_gene(self, gene):
        c = numpy.array(gene[0:self.dim*self.func])
        w = numpy.array(gene[self.dim*self.func:])
        self.center = c.reshape(self.func, self.dim)
        self.weight = w.reshape(self.outputs, self.func)

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


# class for creating and training a particle swarm of RBF neural networks
class ParticleSwarm:
    def __init__(self, dim=2, func=2, outputs=2, particles=30):
        self.dim = dim
        self.func = func
        self.outputs = outputs
        self.num_particles = particles
        self.geno_size = dim*func + func*outputs
        self.particles = [rbfnet(dim, func, outputs) for x in range(particles)]
        self.c1 = 2.0
        self.c2 = 2.0
        for p in self.particles:
            p.randomize()
            p.velocity = numpy.array([random.random() for x in range(self.geno_size)])
            p.best = p.to_gene()
            p.best_score = -1.0
            p.score = -1.0
        self.gbest = [0.0 for x in range(self.geno_size)]
        self.gbest_score = -1.0

    # Compute new values for particles based on score vector
    # p.score vector assumed to be populated prior to calling update
    def update(self):
        for p in self.particles:
            if p.score > p.best_score:
                p.best_score = p.score
                p.best = p.to_gene()
            if p.score > self.gbest_score:
                self.gbest_score = p.score
                self.gbest = p.to_gene()

        for p in self.particles:
            r1 = numpy.array([random.random() for x in range(self.geno_size)])
            r2 = numpy.array([random.random() for x in range(self.geno_size)])
            param = p.to_gene()
            p.velocity = p.velocity + self.c1 * r1 * (p.best - param) + self.c2 * r2 * (self.gbest - param)
            p.from_gene(param + p.velocity)



class Testbench(unittest.TestCase):
    def setUp(self):
        pass

    def test_recode(self):
        for dim in range(2, 6):
            for func in range(2, 6):
                for outputs in range(2, 6):
                    r = rbfnet(dim, func, outputs)
                    r.randomize()
                    g = r.to_gene()
                    r2 = rbfnet(dim, func, outputs)
                    r2.from_gene(g)
                    r2.eval([0.0]*dim)

                    self.assertEqual(r2.to_gene().sum() - g.sum(), 0.0)

    def test_swarm_mult(self):
        pswarm = ParticleSwarm(2, 2, 1)

        for x in range(5):
            # score the particles
            scores = []
            for p in pswarm.particles:
                inp = [random.random(), random.random()]
                r = p.eval(inp)
                p.score = -math.pow(r[0] - inp[0]*inp[1], 2)
                scores.append(p.score)
            #print scores
            pswarm.update()

        self.assertGreater(pswarm.gbest_score, -0.01)


if __name__ == "__main__":
    unittest.main()
