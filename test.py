#!/usr/bin/python
# -*- coding: utf-8 -*-p0
import pydiag
from pydiag import *

p0 = t(0)
t2 = t(3)
t3 = t(2, 5)
t1 = t(2, 3, 7)
t5 = t1 + t3
print t5
t6 = t3 * 5
print t6
print t6 * 3


t0 = t( (1, 1, 1, 0, 1, 1, 0, 0) )

print t6.d( lambda x: x.n )

print t6.d(6)
print t6.d( (1, 2, 3, 4, 5) )
print t6.d( (1, 2, 3, 4, 5, 6, 7, 8, 9, 1) )
print t6.d( (1, 2, 3, 4, 5, 6, 7, 8, 9, 1, 4, 2, 3, 4) )
print t(5).d( lambda x: x.n)
print d(t(3), 5 )

