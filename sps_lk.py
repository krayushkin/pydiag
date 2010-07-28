#!/usr/bin/python
# -*- coding: windows-1251 -*-

from pydiag import *
import struct
import array

uint8 = "B"
uint16 = "H"
uint32 = "I"

MAXNumber16 = 0x10000
CountPlats = 9

class TCycleEvensData:
    def __init__(self):
    #   ���� � ������
    #   quint32 fTn0;   // ���. ��
        self.fTn0 = array.array(uint32, [0] )
    #   quint32 fLength; // ������� �����
        self.fLength = array.array(uint32, [0] )
    #   quint16 fCount; // ���-�� ���������� // 1 - �������������
        self.fCount = array.array(uint16, [0] )
    #   quint16 fDiff; // ������� (�������: 15-14 - 00-���/ 01 - 0/ 10 - 1/ 11 - �� 0 � �� 1
    #   // (�� ���.)// 13-0 - ����� ������ ��������)
        self.fDiff = array.array(uint16, [0] )
    
class TMassData16:
    def __init__(self):
    #   quint16 FMsTs[MAXNumber16];  //������ �����(������� 0/1)
        self.FMsTs = array.array(uint16, [0 for i in xrange(MAXNumber16)] )
    #   quint16 FMsKm[MAXNumber16];  // ������ ����������(������/�����)
        self.FMsKm = array.array(uint16, [0 for i in xrange(MAXNumber16)] )
    #   quint16 FMsMk[MAXNumber16];  // ������ �����(���� /���)
        self.FMsMk = array.array(uint16, [0 for i in xrange(MAXNumber16)] )
    #   quint8 FMskan[16]; // ������������ ������� ������� ������� ��� �������������� (default: 0 � 143 ��� 0 - 95)
        self.FMskan = array.array(uint8, [0 for i in xrange(16)] )
    #   quint8 FMspin[16][11];  // �������� ��������� (����������) (default:��)
        self.FMspin = array.array(uint8, [0 for i in xrange(16*11)] )
    #   quint8 FMsUrov[16][3];  // 0-������ 0    1- ������ 1   2-��.����������� (default: [x,0]:=$80; [x,1]:=$5D; [x,2]:=$76;)
        self.FMsUrov = array.array(uint8, [0 for i in xrange(16*3)] )
    #   quint16 FMskk;         // ����������� ������� (���������  ����/��� ) (default: $FFFF)
        self.FMskk = array.array(uint16, [0] )
    #   quint16 FAdv[16];  //����������������� (default: $0000)
        self.FAdv = array.array(uint16, [0 for i in xrange(16)] )

class ToffsenData16:
    def __init__(self):
    #   quint8 SRea;  //(default: $E1)
        self.SRea = array.array(uint8, [0] )
    #   quint16 FRej;  // (default: $88CA) ��������� ������ (�������): 0-���� 1-���� ��. 2-��� 3 ���� ���. 4-���� 5-�����.��. 6-���� 7-����� 8-11-������� 12-������ �/� 13-������� �/� 14-������� 15-�������
        self.FRej = array.array(uint16, [0] )
    #   quint32 FKolTN; //(default: 65538) ���������� ����-������� +2
        self.FKolTN = array.array(uint32, [0] )
    #   quint8 FKolKan; //(default:146) ���������� ������� +2
        self.FKolKan = array.array(uint8, [0] )
    #   TCycleEvensData FCyc[8];  // ����� (�� ����� 8)
        self.FCyc = [TCycleEvensData() for i in xrange(8)]
    #   quint8 FRezerv[5];       // ������
        self.FRezerv = array.array(uint8, [0 for i in xrange(5)] )
    #   quint8 FMsOst[MAXNumber16]; // ����� �������� 1-����, 2- �����,3- �������, 4-����, 5-�����
        self.FMsOst = array.array(uint8, [0 for i in xrange(MAXNumber16)] )

class FLKData16:
    def __init__(self):
    #    TMassData16 MassData[CountPlats];
        self.MassData = [TMassData16() for i in xrange(CountPlats)]
    #    ToffsenData16 LKData;
        self.LKData = ToffsenData16()

class sps_lk:
    def __init__(self):
        self.lk = FLKData16()
        kan_num = 0
        for i in xrange(CountPlats):
            for k in xrange(16):
                self.lk.MassData[i].FMskan[k] = kan_num;
                kan_num = kan_num + 1
                self.lk.MassData[i].FMsUrov[k*3 + 0] = 0x80;
                self.lk.MassData[i].FMsUrov[k*3 + 1] = 0x5D;
                self.lk.MassData[i].FMsUrov[k*3 + 2] = 0x76;
                self.lk.MassData[i].FMskk[0] = 0xFFFF;
        self.lk.LKData.SRea[0] = 0xE1;
        self.lk.LKData.FRej[0] = 0x88CA | (1<<5);
        self.lk.LKData.FKolTN[0] = 65538;
        self.lk.LKData.FKolKan[0] = 146;        

    def store_params(self, *params):
        

    def write(self, filename):
        # @type filename: string
        with open( filename, "w") as f:
            for MassData_i in self.lk.MassData:
                MassData_i.FMsTs.tofile(f)
                MassData_i.FMsKm.tofile(f)
                MassData_i.FMsMk.tofile(f)
                MassData_i.FMskan.tofile(f)
                MassData_i.FMspin.tofile(f)
                MassData_i.FMsUrov.tofile(f)
                MassData_i.FMskk.tofile(f)
                MassData_i.FAdv.tofile(f)
            self.lk.LKData.SRea.tofile(f)
            self.lk.LKData.FRej.tofile(f)
            self.lk.LKData.FKolTN.tofile(f)
            self.lk.LKData.FKolKan.tofile(f)
            for FCyc_i in self.lk.LKData.FCyc:
                FCyc_i.fTn0.tofile(f)
                FCyc_i.fLength.tofile(f)
                FCyc_i.fCount.tofile(f)
                FCyc_i.fDiff.tofile(f)
            self.lk.LKData.FRezerv.tofile(f)
            self.lk.LKData.FMsOst.tofile(f)

lk = sps_lk()
lk.write("x:/helloo.lk")
