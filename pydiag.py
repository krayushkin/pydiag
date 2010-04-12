#!/usr/bin/python
# -*- coding: utf-8 -*-

reciever


class I:
    pass

class O:
    pass

class M:
    def __init__(self, mask):
        ## TODO Вставить проверку на число
        self.mask = mask

M1 = M(~0)
M0 = M(0)

a.mask | (5 << 1)


# Описывает параметр
# Следующие свойства:
# mask
class param:
    """
    param итерируемый тип:
    p0 = param("1-32", "data")
    p0 << d( t(1, 10) * 3, (1, 2, 4) )
    for i in p0:
        print i
        
    param можно создавать без указания параметров, тогда он не войдет в
    конечный тест, то вы можете использовать его в любых выражениях как
    и обычный param.
    Пример:
    p1 = param()
    p1 << (1, 0, 1, 0, 0, 0, 0) * 3
    """
    

    def __init__(self, chanells = None, name = "UNNAMED", in_out = I, mask = M0)
       self.chanells = self.__parse(chanells)
       self.name = name
       self.in_out = in_out
       self.__repr = [] # _repr tuple of (data, mask, io)


    def __len__(self):
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
                   raise ValueError("Неправильная строка каналов!")
        return res
    
    # other - interable type or single integer
    def __lshift__(self, other):
        if hasattr(other, "__iter__"):
            # other - iterable
            print "iterable detected"
            for i in other:
            __repr.append( () )    
            
        elif isinstance(other, M):
            print "mask detected"
            # other - mask
            # TODO
            pass
        else:
            # single integer
            __data.append(other)
            return self
        
        


def d(time, func_or_iterable_or_int):
    """
    Функция создает кортеж(tuple) данных, которые могут быть
    затем переданы в параметр
    Пример:
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
    Печатает данные в удобном виде
    """    
    print data


class t:
    def __init__(self, *arguments, **keywords):
        print arguments
        print keywords
        pass
    
    def __repr__(self):
        return "time"
        
    def __str__(self):
        return self.__repr__()
    
    # other - t type
    def __add__(self, other):
        pass

    # other - integer
    def __mult__(self, other):
        pass


    def d(self, func_or_iterable_or_int):
        for i in xrange(10):
            self.loop = i
            for k in xrange(10):
                self.takt = i*10 + k
                if (callable(func_or_iterable_or_int)):
                    print func_or_iterable_or_int( self )
                else:
                    it = iter(func_or_iterable_or_int)
        pass


def inv(data):
    """
    Инвертирует данные
    """
    return tuple ( [~data_i for data_i in data] )


x = param("5, 4-14, 3", "hello")
d = t(1, 2)


