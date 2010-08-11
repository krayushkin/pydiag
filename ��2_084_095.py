#!/usr/bin/python
# -*- coding: windows-1251 -*-

from pydiag import *
import sps_lk

prog_name("ca2_084_095")

param("����2", "78,79,81,80,68,74,73,72,56,127,83,71,26,82,128,126", IN, M1)
param("����1", "103, 104, 107, 105, 101, 99, 102, 100, 109, 98, 96, 106, 93, 97, 95, 94", IN, M1) 

p["����2"] << d(t(1, 2)*p["����2"].n_ch, lambda x: 1 << x.p )
p["����1"] << (1, 2, 3)

sps_lk.end()
