#!/usr/bin/python
# -*- coding: windows-1251 -*-

import copy
import numbers

import xml.dom as xml


def get_bit(num, n):
    return 0 if num & (1<<n) == 0 else 1

def store_params(*args):
    channels = {}
    
    for p in args:
        for ch in p.ch:
            if ch not in channels:
                channels[ch] = p
            else:
                raise AssertionError( "Duplicate channel {0} in parameter {1}. Already defined in {2} param.".format(ch, p.name, channells[ch].name) )
                
    
    impl = xml.getDOMImplementation()
    doc = impl.createDocument(None, None, None)
    root = doc.appendChild(doc.createElement("test"))
    
    for ch in channels:
        p = channels[ch]
        index = [index for index, c in enumerate(p.ch) if c == ch][0]
        print "ch = {0}, index = {1}, param_name = {2}".format(ch, index, p.name)
        ch_data = []
        ch_mask = []
        ch_io   = []
        
        for d, m, io in p.dmio_iter():
            ch_data.append(str(get_bit(d, index)))
            ch_mask.append(str(get_bit(m.mask, index)))
            ch_io.append( str(io) )

        ch_data = "".join(ch_data)
        ch_mask = "".join(ch_mask)
        ch_io   = "".join(ch_io)
        
        channel_node = root.appendChild(doc.createElement("channel"))
        channel_node.setAttribute( "id", str(ch) )
        
        if p.n_ch > 1:
            channel_node.setAttribute( "name", "{0}_{1}".format(p.name, index) )
        else:
            channel_node.setAttribute( "name", p.name )
        data_node = channel_node.appendChild(doc.createElement("data"))
        data_node.appendChild(doc.createTextNode(ch_data))
        mask_node = channel_node.appendChild(doc.createElement("mask"))
        mask_node.appendChild(doc.createTextNode(ch_mask))
        io_node = channel_node.appendChild(doc.createElement("io"))
        io_node.appendChild(doc.createTextNode(ch_io))
        
    print doc.toxml()
    
    
    
    
class IN_OUT:
    """
    Класс для установки параметра на вход или выход.
    Например:
    p0 = param("1-32", "data")
    p0 << IN << 5 << OUT << 6
    """
    def __init__(self, in_out):
        if in_out in ("in", "out" ): 
            self.in_out = in_out
        else:
            raise TypeError("Передано неверное значение. Возможные варианты: \"in\" и \"out\" ")
        
    def __str__(self):
        return "I" if self.in_out=="in" else "O"
    
    def __repr__(self):
        return str(self)

IN = IN_OUT("in")
OUT = IN_OUT("out")

class M:
    """
    Объекты этого класса устонавливают маску,
    разрешая или запрещая контроль на заданных разрядах
    параметра
    """
    def __init__(self, mask):
        ## TODO Вставить проверку на число
        self.mask = mask
        
    def __str__(self):
        return str(self.mask)
    
    def __repr__(self):
        return str(self)

M1 = M(~0)
M0 = M(0)



class param:
    """
    param можно создавать без указания параметров, тогда он не войдет в
    конечный тест, то вы можете использовать его в любых выражениях как
    и обычный param.
    Пример:
    p1 = param()
    p1 << (1, 0, 1, 0, 0, 0, 0) * 3
    
    Публичные атрибуты:
        mask - текущая маска
        io - текущее направление сигнала
        n_ch - количество разрядов
        ch - перечень каналов
        name - имя параметра
        
    Поддерживаются два итератора: __iter__() и dmio_iter()
    Первый позоляет перебирать только данные параметра, а второй используется для
    итерации массива всех данных, элементами которых является кортеж (ДАННЫЕ, МАСКА, ВХОД/ВЫХОД)
    """
    
    def __str__(self):
        s = "param {0}:\n".format(self.name)
        if len(self.__repr) > 0:
            d, m, io = zip(*self.__repr) 
            s += "d:  " + str(d) + "\n"
            s += "io: " + str(io) + "\n"       
            s += "m:  " + str(m) + "\n"
        else:
            s += "<--Empty-->\n"
        s += "current mask: " + str(self.mask) + "\n"
        s += "current io: " + str(self.io)+ "\n"
        return s
    
    def __repr__(self):
        return str(self)

    def __init__(self, channels = None, name = "UNNAMED", io = IN, mask = M0):
       # tuple каналов
       self.ch = self.__parse(channels)
       # количество каналов
       self.n_ch = len(self.ch)
       # имя
       self.name = name
       # вход или выход
       self.io = io
       # текущая маска
       self.mask = mask
       
       # список (data, mask, io)
       self.__repr = [] # _repr list of (data, mask, io)
       

    def __len__(self):
        """Количество тестовых наборов в параметре"""
        return len(self.__repr)

    def __iter1_generator(self):
        """ Генератор для первого итератора """
        for d, m, io in self.__repr:
            yield d

    def __iter__(self):
        """
        Первый итератор. Позволяет перебирать элементы типа data.
        Например:
            p1 = param()
            p1 << (1, 0, 1, 0, 0, 0, 0) * 3
            i = 0
            for d in p1:
                print "TN =", i
                print "data =", d
                i = i + 1
        """
        
        return self.__iter1_generator()
    
    def __iter2_generator(self):
        """ Генератор для второго итератора """
        for value in self.__repr:
            yield value

    def dmio_iter(self):
        """
        Второй итератор. Позволяет перебирать элементы типа (data, mask, io), а не
        только data, как в первом итераторе.
        Например:
            p1 = param()
            p1 << (1, 0, 1, 0, 0, 0, 0) * 3
            i = 0
            for d, m, io in p1.dmio_iter():
                print "TN =", i
                print "data =", d, "mask =", m, "io =", io
                i = i + 1
        """
        return self.__iter2_generator()


    def __parse(self, channels):
        """
        Парсит строку каналов
        """
        res = []
        if channels == None or len(channels) == 0:
            return []
        channels = channels.replace(" ", "")
        channels = channels.split(",")
        for group in channels:
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
        """
        other может быть:
            а) Числом
            б) Любым итерируемым типом
            в) Маской (т.е. M1, M0 или любым другим объектом класса M)
            г) Входом или выходом (т.е. IN или OUT)
            д) Кортежем (ДАННЫЕ, МАСКА, ВХОД/ВЫХОД)
        """ 
        if hasattr(other, "__iter__"):
            # Если other - кортеж из (ДАННЫЕ, МАСКА, ВХОД/ВЫХОД)
            if len(other) == 3 and isinstance(other[0], numbers.Number) and isinstance(other[1], M) and isinstance(other[2], IN_OUT):
                self.__repr.append((other[0], other[1], other[2]))
                self.mask = other[1]
                self.io = other[2]
            # Иначе other - массив чисел (numbers.Number)
            else:
                # Проверяем каждый элемент в последовательности (это должен быть numbers.Number)
                for i in other:
                    if not isinstance(i, numbers.Number):
                        raise TypeError("В последовательности найден элемент с неверным типом")
                # Теперь добавляем
                for i in other:
                    self.__repr.append((i, self.mask, self.io))
                
        elif isinstance(other, M):
            self.mask = other
            # other - mask

        elif isinstance(other, IN_OUT):
            self.io = other
            
        elif isinstance(other, numbers.Number):
            # single integer
            self.__repr.append( (other, self.mask, self.io ) )
        else:
            raise TypeError("Неверный тип операнда")
            
        return self

    def __getitem__(self, index):
        """
        Получить информацию о тест наборе с номером index в виде кортежа
        (ДАННЫЕ, МАСКА, ВХОД/ВЫХОД). Нумерация тест наборов начинается с 0.
        """
        return self.__repr[index]

def d(time, func_or_iterable_or_int):
    """
    Функция создает кортеж(tuple) данных из заданного
    временного интервала time и исходных данных
    которые могут быть затем переданы в параметр.
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
    # TODO
    print data


class t:
    """
    Способы создания подробно описаны в фунции __init__.

    Временные интервалы можно складывать:
    t4 = t(3) + t(2, 4)
    Но прибавлять к временному интервалу целое число нельзя:
    t4 = t(3) + 8 # Ошибка!

    Но временной интервал можно умножать на любое положительное
    целое число:
    t5 = t(2, 5) * 8

    Можно совмещать эти операции:
    t6 = (t5 + t3) * 3

    Так же конструировать временные интервалы можно из итерируемых
    типов. Элементами контейнеров могут быть только значения 1 или 0.
    1 означает место в которое будет вставлено конкретное значение
    при конструировании данных.
    t7 = t( (1, 0, 1, 1, 1, 1, 0) )
    """

    def __init__(self, *arguments):
        """
        Первый параметр - длительность в тактах временного отрезка.
        t1 = t(0) # пустой отрезок допустим
        t2 = t(3)

        Второй параметр (опционально) - период в тактах временного
        отрезка:
        t3 = t(2, 4)

        Также класс можно создавать передавая 3 параметра, тогда первый -
        это пауза перед началом импульса или пачки, остальные два - как
        описано выше:
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
                    raise TypeError("Значения в последовательности могут быть только 0 и 1")
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
        """ Количество ТН """
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
        """ Складывает два временных интервала """
        x = copy.deepcopy(self)
        x.__data += other.__data
        x.__period += other.__period
        return x

    # other - integer
    def __mul__(self, other):
        """ Умножение на число """
        x = copy.deepcopy(self)
        p = []
        for i in xrange(other):
            p += [i for temp in xrange(len(x.__data)) ]
        x.__data *= other
        x.__period = p
        return x


    def d(self, func_or_iterable_or_int):
        """ второй параметр может быть:
        а) функция
              может иметь один аргумент, либо вообще их не иметь.
              Первый аргумент - это объект контекста (опционально).
              Через него можно получить такие значения как номер такта,
              период и, в будущих версиях, возможно. ещё что-нибудь будет.
              если сроварь не нужен, то в фунцию можно ничего не передавать.
              В данный момент поддерживаются следующие атрибуты этого объекта x:
                  x.t - номер такта, начиная с 0
                  x.p - период, начиная с 0
                  x.n - текущий номер ненулевого ТН. Т.е. номер, считая только ненулевые ТН. Начиная с 0
              Функция должна возвращать число.
              
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
              
        б) любой итерируемый объект
              объектами должны быть числа.
              если количество элементов в последовательности больше чем ТН в временном
              отрезке, то лишние элементы просто игнорируются.
              если количество элементом меньше чем количество ТН, то конечные ТН будут
              заполнены значением последнего элемента переданной последовательности.
              
              t3 = t(5, 8)
              d0 = t3( ( 1, 2, 3, 3, 2 ) )
              # d = ( 1, 2, 3, 3, 2, 0, 0, 0 )
              
              d1 = t3( ( 1, 2, 3, 3 ) )
              # d = ( 1, 2, 3, 3, 3, 0, 0, 0 )
              
              d2 = t3( ( 1, 2, 3, 3, 2, 1 ) )
              # d = ( 1, 2, 3, 3, 2, 0, 0, 0 )
              
              
        в) число
              во всех ненулевых ТН во временном отрезке вставляется переданное число
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
                    self.p = self.__period[i]
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
    Инвертирует данные
    """
    return tuple ( [~data_i for data_i in data] )
