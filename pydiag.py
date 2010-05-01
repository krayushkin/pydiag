#!/usr/bin/python
# -*- coding: windows-1251 -*-

import copy
from compiler.ast import TryExcept

class IN:
    """
    ����� ��� ��������� ��������� �� ����.
    ��������:
    p0 = param("1-32", "data")
    p0 << IN
    """
    pass

class OUT:
    """����� ��� ��������� ��������� �� ����
    ��������:
    p0 = param("1-32", "data")
    p0 << OUT
    """
    pass

class M:
    """������� ����� ������ ������������� �����,
    �������� ��� �������� �������� �� �������� ��������
    ���������
    """
    def __init__(self, mask):
        ## TODO �������� �������� �� �����
        self.mask = mask

M1 = M(~0)
M0 = M(0)


# ��������� ��������
# ��������� ��������:
# mask
class param:
    """
    param ����������� ���:
    p0 = param("1-32", "data")
    p0 << d( t(1, 10) * 3, (1, 2, 4) )
    for i in p0:
        print i
        
    param ����� ��������� ��� �������� ����������, ����� �� �� ������ �
    �������� ����, �� �� ������ ������������ ��� � ����� ���������� ���
    � ������� param.
    ������:
    p1 = param()
    p1 << (1, 0, 1, 0, 0, 0, 0) * 3
    """
    

    def __init__(self, chanells = None, name = "UNNAMED", in_out = IN, mask = M0):
       
       # tuple �������
       self.chanells = self.__parse(chanells)
       # ���
       self.name = name
       # ���� ��� �����
       self.in_out = in_out
       # ������ (data, mask, io)
       self.__repr = [] # _repr tuple of (data, mask, io)


    def __len__(self):
        """���������� �������� ������� � ���������"""
        return len(self.__repr)


    def __iter__(self):
        # TODO
        return self

    def next(self):
        # TODO
        return
    
    def __parse(self, chanells):
        res = []
        chanells = chanells.replace(" ", "")
        chanells = chanells.split(",")
        for group in chanells:
            if group.isdigit():
                res.append( int( group ) )
            else:
                if group.find("-") != -1:
                    interval = group.split("-")
                    a, b = interval
                    a = int(a)
                    b = int(b)
                    if a < b:
                        for i in xrange(a, b+1):
                            res.append( i )
                    else:
                        for i in xrange(a, b-1, -1):
                            res.append( i )
                else:
                   raise ValueError("������������ ������ �������!")
        return res
    
    # other - interable type or single integer
    def __lshift__(self, other):
        if hasattr(other, "__iter__"):
            # other - iterable
            print "iterable detected"
            for i in other:
                self.__repr.append((i))
                
        elif isinstance(other, M):
            print "mask detected"
            # other - mask
            # TODO
            pass
            
        elif isinstance(other, IN):
            pass
            
        elif isinstance(other, OUT):
            pass
            
        else:
            # single integer
            __data.append(other)
            return self
        
        


def d(time, func_or_iterable_or_int):
    """
    ������� ������� ������(tuple) ������ �� ���������
    ���������� ��������� time � �������� ������
    ������� ����� ���� ����� �������� � ��������.
    ������:
    p0 = param("1-32", "data")
    p1 = param("33-64", "data2")
    
    p0 << d( t(1, 10) * 3, (1, 2, 4) )
    p0 << d( t(3), lambda x: x.takt )
    p1 << d( t(1), 5) + d(t(10), lambda x: x.takt )
    data = (1, 0, 0, 0, 0, 1, 1, 1, 0) * 20
    p1 << d( t( len(data)), data)
    p1 << d( t(1), 500 ) * 100
    """
    return time.d(func_or_iterable_or_int)



def printd(data):
    """
    �������� ������ � ������� ����
    """
    # TODO
    print data


class t:
    """
    ������� �������� �������� ������� � ������ __init__.

    ��������� ��������� ����� ����������:
    t4 = t(3) + t(2, 4)
    �� ���������� � ���������� ��������� ����� ����� ������:
    t4 = t(3) + 8 # ������!

    �� ��������� �������� ����� �������� �� ����� �������������
    ����� �����:
    t5 = t(2, 5) * 8

    ����� ��������� ��� ��������:
    t6 = (t5 + t3) * 3

    ��� �� �������������� ��������� ��������� ����� �� �����������
    �����. ���������� ����������� ����� ���� ������ �������� 1 ��� 0.
    1 �������� ����� � ������� ����� ��������� ���������� ��������
    ��� ��������������� ������.
    t7 = t( (1, 0, 1, 1, 1, 1, 0) )
    """

    def __init__(self, *arguments):
        """
        ������ �������� - ������������ � ������ ���������� �������.
        t1 = t(0) # ������ ������� ��������
        t2 = t(3)

        ������ �������� (�����������) - ������ � ������ ����������
        �������:
        t3 = t(2, 4)

        ����� ����� ����� ��������� ��������� 3 ���������, ����� ������ -
        ��� ����� ����� ������� �������� ��� �����, ��������� ��� - ���
        ������� ����:
        t1 = (2, 3, 5)
        """
        self.__data = []
        self.__period = []
        ontime = 0
        pause = 0
        offtime = 0
        if len(arguments) == 3:
            ontime = arguments[1]
            offtime = arguments[2] - ontime
            pause = arguments[0]
        elif len(arguments) == 2:
            ontime = arguments[0]
            offtime = arguments[1] - ontime
            pause = 0
        elif len(arguments) == 1:
            if hasattr( arguments[0], "__iter__"):
                if len(filter(lambda x: x != 0 and x != 1, arguments[0])) != 0:
                    raise TypeError("�������� � ������������������ ����� ���� ������ 0 � 1")
                self.__data = list( arguments[0] )
                for i in xrange(len(self.__data)):
                    self.__period.append(0)
                return
            else:
                ontime = arguments[0]
                offtime = 0
                pause = 0
        
        for i in xrange(pause):
            self.__data.append(0)
            
        for i in xrange(ontime):
            self.__data.append(1)
            
        for i in xrange(offtime):
            self.__data.append(0)

        for i in xrange(ontime + offtime + pause):
            self.__period.append(0)
    
    def __len__(self):
        """ ���������� �� """
        return len(self.__data)
    
    def __repr__(self):
        def pattern(l):
            string = ""
            for i in l:
                if i == 0: string += str(i)
                else: string += str(i)
            return string
        return "d: {0}\np: {1}\n".format(pattern(self.__data), pattern(self.__period))

    def __str__(self):
        return self.__repr__()
    
    # other - t type
    def __add__(self, other):
        """ ���������� ��� ��������� ��������� """
        x = copy.deepcopy(self)
        x.__data += other.__data
        x.__period += other.__period
        return x

    # other - integer
    def __mul__(self, other):
        """ ��������� �� ����� """
        x = copy.deepcopy(self)
        p = []
        for i in xrange(other):
            p += [i for temp in xrange(len(x.__data)) ]
        x.__data *= other
        x.__period = p
        return x


    def d(self, func_or_iterable_or_int):
        """ ������ �������� ����� ����:
        �) �������
              ����� ����� ���� ��������, ���� ������ �� �� �����.
              ������ �������� - ��� ������ ��������� (�����������).
              ����� ���� ����� �������� ����� �������� ��� ����� �����,
              ������ �, � ������� �������, ��������. ��� ���-������ �����.
              ���� ������� �� �����, �� � ������ ����� ������ �� ����������.
              � ������ ������ �������������� ��������� �������� ����� ������� x:
                  x.t - ����� �����, ������� � 0
                  x.p - ������, ������� � 0
                  x.n - ������� ����� ���������� ��. �.�. �����, ������ ������ ��������� ��. ������� � 0
              ������� ������ ���������� �����.
              
              t3 = t(2, 4)
              t3.d( lambda: 0 )
              t3.d( lambda x: x.t + 2)
              
              def func0( x ):
                  a = x.t + x.p
                  return a / 2

              import random
            
              def func1():
                  return random.random()
                   
              t3.d(func)
              
        �) ����� ����������� ������
              ��������� ������ ���� �����.
              ���� ���������� ��������� � ������������������ ������ ��� �� � ���������
              �������, �� ������ �������� ������ ������������.
              ���� ���������� ��������� ������ ��� ���������� ��, �� �������� �� �����
              ��������� ��������� ���������� �������� ���������� ������������������.
              
              t3 = t(5, 8)
              d0 = t3( ( 1, 2, 3, 3, 2 ) )
              # d = ( 1, 2, 3, 3, 2, 0, 0, 0 )
              
              d1 = t3( ( 1, 2, 3, 3 ) )
              # d = ( 1, 2, 3, 3, 3, 0, 0, 0 )
              
              d2 = t3( ( 1, 2, 3, 3, 2, 1 ) )
              # d = ( 1, 2, 3, 3, 2, 0, 0, 0 )
              
              
        �) �����
              �� ���� ��������� �� �� ��������� ������� ����������� ���������� �����
              t3 = t(5, 8)
              d0 = t3( 7 )
              # d = ( 7, 7, 7, 7, 7, 0, 0, 0 )
              
              t3 = t(5)
              d0 = t3( 7 )
              # d = ( 7, 7, 7, 7, 7 )
              
              """
        result = []
              
        if hasattr(func_or_iterable_or_int, "__call__"):
            """ callable """
            self.n = 0
            for i in xrange( len(self.__data) ):
                if self.__data[i] == 1:
                    self.t = i
                    self.p = self.__period
                    try:
                        result.append( func_or_iterable_or_int() )
                    except TypeError:
                        result.append( func_or_iterable_or_int(self) )
                    self.n += 1
                else:
                     result.append(0)
                     
        elif hasattr(func_or_iterable_or_int, "__iter__"):
            """ iterable """
            l = [x for x in func_or_iterable_or_int]
            l_it = iter( l )
            for i in xrange( len(self.__data) ):
                if self.__data[i] == 1:
                    try:
                        result.append( l_it.next() )
                    except StopIteration:
                        result.append( l[ len(l) - 1 ] )
                else:
                     result.append(0)
                
        else:
            """ int """
            for i in xrange( len(self.__data) ):
                if self.__data[i] == 1:
                    result.append( func_or_iterable_or_int )
                else:
                    result.append(0)
                    
        return result

def inv(data):
    """
    ����������� ������
    """
    return tuple ( [~data_i for data_i in data] )
