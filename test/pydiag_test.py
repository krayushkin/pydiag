#!/usr/bin/python
# -*- coding: windows-1251 -*-


from pydiag import *
import unittest

class  ParamTestCase(unittest.TestCase):
    #def setUp(self):
    #    self.foo = New_()
    #

    #def tearDown(self):
    #    self.foo.dispose()
    #    self.foo = None

    def test_std_iterator(self):
        p1 = param("10, 12, 23, 30-24, 32-40, 2, 1" , "DATA", IN, M1)
        p1 << 5 << OUT << 10 << (2, 3, 4, 6) << M0 << xrange(5) << (90, M1, IN)
        p1_d = [5, 10, 2, 3, 4, 6, 0, 1, 2, 3, 4, 90]
        
        # d iterator 1 test
        d1 = iter(p1)
        self.assertEqual(d1.next(), p1_d[0])
        self.assertEqual(d1.next(), p1_d[1])
        self.assertEqual(d1.next(), p1_d[2])
        self.assertEqual(d1.next(), p1_d[3])
        d2 = iter(p1)
        self.assertEqual(d2.next(), p1_d[0])
        self.assertEqual(d2.next(), p1_d[1])
        self.assertEqual(d2.next(), p1_d[2])
        self.assertEqual(d2.next(), p1_d[3])

        self.assertEqual(d1.next(), p1_d[4])
        self.assertEqual(d1.next(), p1_d[5])
        self.assertEqual(d1.next(), p1_d[6])
        self.assertEqual(d1.next(), p1_d[7])

        self.assertEqual(d2.next(), p1_d[4])
        self.assertEqual(d2.next(), p1_d[5])

        self.assertEqual(d1.next(), p1_d[8])
        self.assertEqual(d1.next(), p1_d[9])
        self.assertEqual(d1.next(), p1_d[10])
        self.assertEqual(d1.next(), p1_d[11])
        self.assertRaises(StopIteration, d1.next)

        self.assertEqual(d2.next(), p1_d[6])
        self.assertEqual(d2.next(), p1_d[7])
        self.assertEqual(d2.next(), p1_d[8])
        self.assertEqual(d2.next(), p1_d[9])
        self.assertEqual(d2.next(), p1_d[10])
        self.assertEqual(d2.next(), p1_d[11])
        self.assertRaises(StopIteration, d2.next)

    def test_dmio_iterator(self):
        p1 = param("10, 12, 23, 30-24, 32-40, 2, 1" , "DATA", IN, M1)
        p1 << 5 << OUT << 10 << (2, 3, 4, 6) << M0 << xrange(5) << (90, M1, IN)
        p1_d = [5, 10, 2, 3, 4, 6, 0, 1, 2, 3, 4, 90]
        p1_m = [M1, M1, M1, M1, M1, M1, M0, M0, M0, M0, M0, M1]
        p1_io = [IN, OUT, OUT, OUT, OUT, OUT, OUT, OUT, OUT, OUT, OUT, IN]
        p1_dmio = zip(p1_d, p1_m, p1_io)
        
        # dmio iterator 1 test
        dmio1 = p1.dmio_iter()
        self.assertEqual(dmio1.next(), p1_dmio[0])
        self.assertEqual(dmio1.next(), p1_dmio[1])
        self.assertEqual(dmio1.next(), p1_dmio[2])
        self.assertEqual(dmio1.next(), p1_dmio[3])
        dmio2 = p1.dmio_iter()
        self.assertEqual(dmio2.next(), p1_dmio[0])
        self.assertEqual(dmio2.next(), p1_dmio[1])
        self.assertEqual(dmio2.next(), p1_dmio[2])
        self.assertEqual(dmio2.next(), p1_dmio[3])

        self.assertEqual(dmio1.next(), p1_dmio[4])
        self.assertEqual(dmio1.next(), p1_dmio[5])
        self.assertEqual(dmio1.next(), p1_dmio[6])
        self.assertEqual(dmio1.next(), p1_dmio[7])

        self.assertEqual(dmio2.next(), p1_dmio[4])
        self.assertEqual(dmio2.next(), p1_dmio[5])

        self.assertEqual(dmio1.next(), p1_dmio[8])
        self.assertEqual(dmio1.next(), p1_dmio[9])
        self.assertEqual(dmio1.next(), p1_dmio[10])
        self.assertEqual(dmio1.next(), p1_dmio[11])
        self.assertRaises(StopIteration, dmio1.next)

        self.assertEqual(dmio2.next(), p1_dmio[6])
        self.assertEqual(dmio2.next(), p1_dmio[7])
        self.assertEqual(dmio2.next(), p1_dmio[8])
        self.assertEqual(dmio2.next(), p1_dmio[9])
        self.assertEqual(dmio2.next(), p1_dmio[10])
        self.assertEqual(dmio2.next(), p1_dmio[11])
        self.assertRaises(StopIteration, dmio2.next)

    def test_shift(self):
        p1 = param("10, 12, 23, 30-24, 32-40, 2, 1" , "DATA", IN, M1)

        p1 << 5 << OUT << 10 << (2, 3, 4, 6) << M0 << xrange(5) << (90, M1, IN)

        p1_d = [d for d, m, io in p1.dmio_iter()]
        self.assertEqual(p1_d, [5, 10, 2, 3, 4, 6, 0, 1, 2, 3, 4, 90])

        p1_m = [m for d, m, io in p1.dmio_iter()]
        self.assertEqual(p1_m, [M1, M1, M1, M1, M1, M1, M0, M0, M0, M0, M0, M1])
        
        p1_io = [io for d, m, io in p1.dmio_iter()]
        self.assertEqual(p1_io, [IN, OUT, OUT, OUT, OUT, OUT, OUT, OUT, OUT, OUT, OUT, IN])

        p1_dmio = zip(p1_d, p1_m, p1_io)
        for i in xrange(12):
            self.assertEqual(p1[i], p1_dmio[i])

        self.assertEqual(p1.mask, M1, "Ошибка маски")
        self.assertEqual(p1.io, IN, "IN OUT error")
        self.assertEqual(len(p1), 12, "Invalid len")

    def test_init(self):
        p0 = param()
        self.assertEqual(p0.ch, [], "Список каналов не пуст")
        self.assertEqual(p0.n_ch, 0, "Количество каналов не равно 0")

        p1 = param("10, 12, 23, 30-24, 32-40, 2, 1" , "DATA", IN, M1)
        self.assertEqual(p1.ch, [10, 12, 23, 30, 29, 28, 27, 26, 25, 24, 32, 33, 34, 35, 36, 37, 38, 39, 40, 2, 1], "Список каналов неверен")
        self.assertEqual(p1.n_ch, 21, "Неверное количество каналов")
        self.assertEqual(p1.mask, M1, "Ошибка маски")
        self.assertEqual(p1.io, IN, "IN OUT error")
        self.assertEqual(p1.name, "DATA", "IN OUT error")
            

if __name__ == '__main__':
    unittest.main()

