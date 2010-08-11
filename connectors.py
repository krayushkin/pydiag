#!/usr/bin/python
# -*- coding: utf8 -*-

def to_c135(s):
    d = {}
    n = 1
    for suff in ("a", "b", "c"):
        for i in xrange(1, 46):
            d[n] = str(i) + suff
            n = n + 1
    return d[s]

def from_c135(s):
    d = {}
    n = 1
    for suff in ("a", "b", "c"):
        for i in xrange(1, 46):
            d[str(i) + suff] = n
            n = n + 1
    return d[s.lower()]

print [to_c135(i) for i in (2, 3, 4, 5, 6, 78)]
print [to_c135(i) for i in (2, 3, 4, 5, 6, 78)]
