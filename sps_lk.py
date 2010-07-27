#!/usr/bin/python
# -*- coding: windows-1251 -*-

from pydiag import *
import struct
import array

"""
const int MAXNumber16 = 0x10000;
const int CountPlats = 9;


/*
��� ���������� ���������� ������ ����� ���������� ������������, � ������:
������� ��������-�������(��) �  ���������� ����� ���� 16���
(�.�. MAXNumber16=$FFFF)
���������� ����� ��������� ���� ������� � 0 (���. ����� �������� 16 �������,
���������� �� ����������  ������ �������)  ��� �������-�
(144��� - CountPlats=8),�������-��(96��� - CountPlats=5)
*/



 // ���� � ������
struct TCycleEvensData
{
   quint32 fTn0;   // ���. ��
   quint32 fLength; // ������� �����
   quint16 fCount; // ���-�� ���������� // 1 - �������������
   quint16 fDiff; // ������� (�������: 15-14 - 00-���/ 01 - 0/ 10 - 1/ 11 - �� 0 � �� 1
                 // (�� ���.)// 13-0 - ����� ������ ��������)
};

// ����� ������
struct ToffsenData16
{
    quint8 SRea;  //(default: $E1)
    quint16 FRej;  // (default: $88CA) ��������� ������ (�������): 0-���� 1-���� ��. 2-��� 3 ���� ���. 4-���� 5-�����.��. 6-���� 7-����� 8-11-������� 12-������ �/� 13-������� �/� 14-������� 15-�������
    quint32 FKolTN; //(default: 65538) ���������� ����-������� +2
    quint8 FKolKan; //(default:146) ���������� ������� +2
    TCycleEvensData FCyc[8];  // ����� (�� ����� 8)
    quint8 FRezerv[5];       // ������
    quint8 FMsOst[MAXNumber16]; // ����� �������� 1-����, 2- �����,3- �������, 4-����, 5-�����
};

// ������ Univer16
struct FLKData16
{
    TMassData16 MassData[CountPlats];
    ToffsenData16 LKData;
};

"""

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
        self.FMsTsFMsKm = array.array(uint16, [0 for i in xrange(MAXNumber16)] )
    #   quint16 FMsMk[MAXNumber16];  // ������ �����(���� /���)
        self.FMsTsFMsMk = array.array(uint16, [0 for i in xrange(MAXNumber16)] )
    #   quint8 FMskan[16]; // ������������ ������� ������� ������� ��� �������������� (default: 0 � 143 ��� 0 - 95)
        self.FMsTsFMskan = array.array(uint8, [0 for i in xrange(16)] )
    #   quint8 FMspin[16][11];  // �������� ��������� (����������) (default:��)
        self.FMsTsFMspin = array.array(uint8, [0 for i in xrange(16*11)] )
    #   quint8 FMsUrov[16][3];  // 0-������ 0    1- ������ 1   2-��.����������� (default: [x,0]:=$80; [x,1]:=$5D; [x,2]:=$76;)
        self.FMsTsFMsUrov = array.array(uint8, [0 for i in xrange(16*3)] )
    #   quint16 FMskk;         // ����������� ������� (���������  ����/��� ) (default: $FFFF)
        self.FMsTsFMskk = array.array(uint16, [0] )
    #   quint16 FAdv[16];  //����������������� (default: $0000)
        self.FMsTsFAdv = array.array(uint16, [0 for i in xrange(16)] )

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

    def write(self, filename):
        # @type filename: string
        with open("w", filename) as f:
            for MassData_i in self.lk.MassData:
                # @type MassData_i: TMassData16
                # @todo: write
                pass

            
    
    
#// ����� ������
#struct ToffsenData16
#{



#};
    
        

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
    root = doc.appendChild(doc.createElement("pydiag-test"))
    root.setAttribute("version", "0.1")
    info_node = root.appendChild(doc.createElement("info"))
    chgroups_node = info_node.appendChild(doc.createElement("chgroup"))
    
    max_len = max( [len(p) for p in args] )
    for p in args:
        p.expand(max_len)
    
    ch_list_sorted = sorted([key for key in channels], key = lambda i: i)
    root.setAttribute("channels", ",".join( [str(i) for i in ch_list_sorted]))


    for p in args:
        group_node = chgroups_node.appendChild(doc.createElement("group"))
        group_node.setAttribute("name", str(p.name))
        # @type p param
        group_node.setAttribute("channels", ",".join( [str(i) for i in p.ch ]))

        #��������� ����������� ���� ��� ����
        if len( p.comments ) != 0:
                group_comments_node = group_node.appendChild(doc.createElement("comments"))
                for tn in sorted([i for i in p.comments], key = lambda item: item ):
                    comment_node = group_comments_node.appendChild(doc.createElement("comment"))
                    comment_node.setAttribute("tn", str(tn))
                    comment_node.setAttribute("content", p.comments[tn])
                    

    for tn in xrange(max_len):
        tn_node = root.appendChild(doc.createElement("tn"))
        tn_node.setAttribute("number", str(tn))
        
        tn_data = []
        tn_mask = []
        tn_io   = []
        for ch in ch_list_sorted:
            p = channels[ch]
            tn_data.append( str (get_bit(p[tn][0], p.nbit(ch))) )
            tn_mask.append( str( get_bit(p[tn][1].mask, p.nbit(ch))))
            tn_io.append( str(  p[tn][2] ))
        tn_data = "".join(tn_data)
        tn_mask = "".join(tn_mask)
        tn_io = "".join(tn_io)

        tn_node.setAttribute("data", tn_data)
        tn_node.setAttribute("mask", tn_mask)
        tn_node.setAttribute("io", tn_io)

    print doc.toprettyxml()