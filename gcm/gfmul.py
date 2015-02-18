#!/usr/bin/env python

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

h = 0x66e94bd4ef8a2c3b884cfa59ca342b2eL
c = 0x0388dace60b6a392f328c2b971b2fe78L
exphash = 0xf38cbb1ad69223dcc3457ae5b6b0f885L

r1 = gfmul(h, c)
r2 = gfmul(h, r1 ^ 0x80)

print "%x" % r2
print "%x" % exphash
