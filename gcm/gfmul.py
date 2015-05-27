#!/usr/bin/env python

import unittest
import numpy

gfpoly = 0xe1 << 120

def gfmul(x, y):
    v = x
    z = 0
    for i in range(127,-1,-1):
        if (y >> i) & 1L == 1:
            z = z ^ v
        if v & 1L == 1:
            v = (v >> 1) ^ gfpoly
        else:
            v = v >> 1
    return z

class TestPoly(unittest.TestCase):
    def test_poly1(self):
        h = 0x66e94bd4ef8a2c3b884cfa59ca342b2eL
        c = 0x0388dace60b6a392f328c2b971b2fe78L
        exphash = 0xf38cbb1ad69223dcc3457ae5b6b0f885L

        r1 = gfmul(h, c)
        r2 = gfmul(h, r1 ^ 0x80)

        self.assertEquals(r2, exphash)

    def test_zero(self):
        r = gfmul(0, 0)
        self.assertEquals(r, 0)

if __name__ == '__main__':
    unittest.main()
