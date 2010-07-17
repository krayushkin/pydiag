#!/usr/bin/python
# -*- coding: windows-1251 -*-


from pydiag import *
import unittest

class HelperFuncTest(unittest.TestCase):
    def test_store_param(self):
        wr = param("1", "#WR", IN)
        rd = param("3", "#RD" , IN)
        data = param("15-23", "#DATA", IN)
        wr << "����� ������" << IN << (2, 4, 65, 67, 2, 3, 4) << "������ �����������" << OUT << 3 << 6 << "�����" << M0 << 7 <<  M1 << "����� �����" << 34 << "��������� ��" << 45
        rd << "������ �����" << 1 << 0 << 1 << 1 << 1 << 0
        data << "������" << d(t(1)*10, lambda x: x.t)
        store_params(wr, rd, data)

class  TTestCase(unittest.TestCase):
    def test_add_mult(self):

        t0 = t(3) + t(2, 5)
        self.assertEqual(t0.data(), [1, 1, 1, 1, 1, 0, 0, 0])
        self.assertEqual(t0.period(), [0, 0, 0, 0, 0, 0, 0, 0])

        t1 = t() + t(2, 3, 7)
        self.assertEqual(t1.data(), [0, 0, 1, 1, 1, 0, 0, 0, 0])
        self.assertEqual(t1.period(), [0, 0, 0, 0, 0, 0, 0, 0, 0])

        t2 = t(3) + t(2, 5) + t1 + t() + t(0)
        self.assertEqual(t2.data(), [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0])
        self.assertEqual(t2.period(), [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

        t6 = t(0, 5)
        self.assertEqual(t6.data(), [0, 0, 0, 0, 0])
        self.assertEqual(t6.period(), [0, 0, 0, 0, 0])

        self.assertRaises(ValueError, t, 4, 0)

        t8 = t(0, 0)
        self.assertEqual(t8.data(), [])
        self.assertEqual(t8.period(), [])
        
        t9 = t(0, 3, 6)
        self.assertEqual(t9.data(), [1, 1, 1, 0, 0, 0])
        self.assertEqual(t9.period(), [0, 0, 0, 0, 0, 0])

        t10 = t(4, 0, 6)
        self.assertEqual(t10.data(), [0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        self.assertEqual(t10.period(), [0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

        self.assertRaises(ValueError, t, 7, 3, 0)

        t3 = t0 * 0
        self.assertEqual(t3.data(), [])
        self.assertEqual(t3.period(), [])
        self.assertEqual(len(t3), 0)

        t4 = t0 * 1
        self.assertEqual(t4.data(), [1, 1, 1, 1, 1, 0, 0, 0])
        self.assertEqual(t4.period(), [0, 0, 0, 0, 0, 0, 0, 0])
        self.assertEqual(len(t3), 0)

        t5 = t0 * 3
        self.assertEqual(t5.data(), [1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0])
        self.assertEqual(t5.period(), [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2])

        t11 = t5 + t5
        self.assertEqual(t11.data(), [1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0] * 2)
        self.assertEqual(t11.period(), [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2])

        t12 = t5 * 2
        self.assertEqual(t12.data(), [1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0] * 2)
        self.assertEqual(t12.period(), [0] * 24 + [1] * 24)

        t13 = (t5 + t(2)) * 3
        self.assertEqual(t13.data(), [1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1] * 3)
        self.assertEqual(t13.period(), [0]*26 + [1]*26 + [2]*26 )

    def test_init(self):
        t0 = t()
        self.assertEqual(t0.data(), [])
        self.assertEqual(t0.period(), [])

        t1 = t(0)
        self.assertEqual(t1.data(), [])
        self.assertEqual(t1.period(), [])

        t2 = t(3)
        self.assertEqual(t2.data(), [1, 1, 1])
        self.assertEqual(t2.period(), [0, 0, 0])

        t3 = t(2, 5)
        self.assertEqual(t3.data(), [1, 1, 0, 0, 0])
        self.assertEqual(t3.period(), [0, 0, 0, 0, 0])

        t4 = t(2, 3, 7)
        self.assertEqual(t4.data(), [0, 0, 1, 1, 1, 0, 0, 0, 0])
        self.assertEqual(t4.period(), [0, 0, 0, 0, 0, 0, 0, 0, 0])

        t5 = t((1, 1, 0, 0, 1, 1, 0, 1))
        self.assertEqual(t5.data(), [1, 1, 0, 0, 1, 1, 0, 1])
        self.assertEqual(t5.period(), [0, 0, 0, 0, 0, 0, 0, 0])

class  ParamTestCase(unittest.TestCase):
    def test_nbit(self):
        p1 = param("10, 12, 23, 30-24, 32-40, 2, 1" , "DATA", IN, M1)
        for i, ch in enumerate(p1.ch):
            self.assertEqual(p1.nbit(ch), i)
        self.assertRaises(ValueError, p1.nbit, 0)
        self.assertRaises(ValueError, p1.nbit, 3)
        self.assertRaises(ValueError, p1.nbit, 500)

    def test_expand(self):
        p1 = param("10, 12, 23, 30-24, 32-40, 2, 1" , "DATA", IN, M1)
        p1.expand(15)
        self.assertEqual( [i for i in p1.dmio_iter()], zip((0,)*15, (M1,)*15, (IN,)*15))
        self.assertEqual( len(p1), 15)
        
        p2 = param("10, 12, 23, 30-24, 32-40, 2, 1" , "DATA", IN, M1)
        p2 << 5 << OUT << 10 << (2, 3, 4, 6) << M0 << xrange(5) << (90, M1, IN)
        p2.expand(15)
        p2_d = [5, 10, 2, 3, 4, 6, 0, 1, 2, 3, 4, 90, 90, 90, 90]
        p2_m = [M1, M1, M1, M1, M1, M1, M0, M0, M0, M0, M0, M1, M1, M1, M1]
        p2_io = [IN, OUT, OUT, OUT, OUT, OUT, OUT, OUT, OUT, OUT, OUT, IN, IN, IN, IN]
        p2_dmio = zip(p2_d, p2_m, p2_io)
        self.assertEqual( [i for i in p2.dmio_iter()], p2_dmio )
        self.assertEqual( len(p2), 15)

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


        p1 << "��������� ���������"

        p1 << 5 << "������������� �� �����"
        p1 << OUT << 10 << (2, 3, 4, 6) << "�����"
        p1 << M0 << xrange(5) << "� ��������� ��" << (90, M1, IN)

        p1_d = [d for d, m, io in p1.dmio_iter()]
        self.assertEqual(p1_d, [5, 10, 2, 3, 4, 6, 0, 1, 2, 3, 4, 90])

        p1_m = [m for d, m, io in p1.dmio_iter()]
        self.assertEqual(p1_m, [M1, M1, M1, M1, M1, M1, M0, M0, M0, M0, M0, M1])
        
        p1_io = [io for d, m, io in p1.dmio_iter()]
        self.assertEqual(p1_io, [IN, OUT, OUT, OUT, OUT, OUT, OUT, OUT, OUT, OUT, OUT, IN])

        p1_dmio = zip(p1_d, p1_m, p1_io)
        for i in xrange(12):
            self.assertEqual(p1[i], p1_dmio[i])

        self.assertEqual(len(p1.comments), 4)
        self.assertEqual(p1.comments[0], "��������� ���������")
        self.assertEqual(p1.comments[1], "������������� �� �����")
        self.assertEqual(p1.comments[6], "�����")
        self.assertEqual(p1.comments[11], "� ��������� ��")

        self.assertEqual(p1.mask, M1, "������ �����")
        self.assertEqual(p1.io, IN, "IN OUT error")
        self.assertEqual(len(p1), 12, "Invalid len")

    def test_init(self):
        p0 = param()
        self.assertEqual(p0.ch, [], "������ ������� �� ����")
        self.assertEqual(p0.n_ch, 0, "���������� ������� �� ����� 0")

        p1 = param("10, 12, 23, 30-24, 32-40, 2, 1" , "DATA", IN, M1)
        self.assertEqual(p1.ch, [10, 12, 23, 30, 29, 28, 27, 26, 25, 24, 32, 33, 34, 35, 36, 37, 38, 39, 40, 2, 1], "������ ������� �������")
        self.assertEqual(p1.n_ch, 21, "�������� ���������� �������")
        self.assertEqual(p1.mask, M1, "������ �����")
        self.assertEqual(p1.io, IN, "IN OUT error")
        self.assertEqual(p1.name, "DATA", "IN OUT error")
            

if __name__ == '__main__':
    unittest.main()

