#!/usr/bin/python
# -*- coding: utf-8 -*-p0

from pydiag import *

print IN
print OUT

wr = param("1", "#WR", IN)
rd = param("3", "#RD" , IN) 
ad = param("4-6", "ADDR", IN)
data = param("15-17", "#DATA", IN)

addr_max = 2 ** ad.n_ch

ad = d( (t(0, 3) + t(5) + t(0, 3)) * addr_max, lambda x: x.p)

wr << IN <<(2, 4, 65, 67, 2,3,4) << OUT << 3 << 6 << M0 << 7 << M1 << 34 << 45

print "address:"
print wr



iter1 = iter(wr)
iter2 = iter(wr)
print "2: ", iter1.next()
print "4: ", iter1.next()
print "65: ", iter1.next()
print "2: ", iter2.next()
print "4: ", iter2.next()
print "65: ", iter2.next()
print "67: ", iter1.next()
print "2: ", iter1.next()
print "67: ", iter2.next()
print "2: ", iter2.next()
print "3: ", iter2.next()

t2 = t(3)
t3 = t(2, 5)
t1 = t(2, 3, 7)
t5 = t1 + t3
print t5
t6 = t3 * 5
print t6
print t6 * 3

def func(x):
    print (x.n, x.t, x.p)
    return 9

t0 = t( (1, 1, 1, 0, 1, 1, 0, 0) )

print t6.d( func )

'''
              _   _
can1     |  _| |_| |_
         |    ___   _
can2     |  _|   |_| |_
         |
cn       |  ___________
         |  
ok       |  ___________
 
 
'''

print t6.d(6)
print t6.d( (1, 2, 3, 4, 5) )
print t6.d( (1, 2, 3, 4, 5, 6, 7, 8, 9, 1) )
print t6.d( (1, 2, 3, 4, 5, 6, 7, 8, 9, 1, 4, 2, 3, 4) )
print t(5).d( lambda x: x.n)
print d(t(3), 5 )

