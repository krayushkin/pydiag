#!/usr/bin/python
# -*- coding: utf8 -*-


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
    #   инфа о циклах
    #   quint32 fTn0;   // нач. ТН
        self.fTn0 = array.array(uint32, [0] )
    #   quint32 fLength; // глубина цикла
        self.fLength = array.array(uint32, [0] )
    #   quint16 fCount; // кол-во повторений // 1 - бесконечность
        self.fCount = array.array(uint16, [0] )
    #   quint16 fDiff; // перепад (побитно: 15-14 - 00-нет/ 01 - 0/ 10 - 1/ 11 - по 0 и по 1
    #   // (не исп.)// 13-0 - номер канала перепада)
        self.fDiff = array.array(uint16, [0] )
    
class TMassData16:
    def __init__(self):
    #   quint16 FMsTs[MAXNumber16];  //массив теста(уровень 0/1)
        self.FMsTs = array.array(uint16, [0 for i in xrange(MAXNumber16)] )
    #   quint16 FMsKm[MAXNumber16];  // массив коммутации(приемн/перед)
        self.FMsKm = array.array(uint16, [0 for i in xrange(MAXNumber16)] )
    #   quint16 FMsMk[MAXNumber16];  // массив маски(выкл /вкл)
        self.FMsMk = array.array(uint16, [0 for i in xrange(MAXNumber16)] )
    #   quint8 FMskan[16]; // соответствие номеров каналов строкам при перетаскивании (default: 0 – 143 или 0 - 95)
        self.FMskan = array.array(uint8, [0 for i in xrange(16)] )
    #   quint8 FMspin[16][11];  // название контактов (примечание) (default:’’)
        self.FMspin = array.array(uint8, [0 for i in xrange(16*11)] )
    #   quint8 FMsUrov[16][3];  // 0-уровни 0    1- уровни 1   2-ур.компаратора (default: [x,0]:=$80; [x,1]:=$5D; [x,2]:=$76;)
        self.FMsUrov = array.array(uint8, [0 for i in xrange(16*3)] )
    #   quint16 FMskk;         // отображение каналов (побитовое  выкл/вкл ) (default: $FFFF)
        self.FMskk = array.array(uint16, [0] )
    #   quint16 FAdv[16];  //зарезервированный (default: $0000)
        self.FAdv = array.array(uint16, [0 for i in xrange(16)] )

class ToffsenData16:
    def __init__(self):
    #   quint8 SRea;  //(default: $E1)
        self.SRea = array.array(uint8, [0] )
    #   quint16 FRej;  // (default: $88CA) параметры режима (побитно): 0-внеш 1-брак ур. 2-шаг 3 брак фун. 4-цикл 5-удерж.ур. 6-стоп 7-конец 8-11-частота 12-запуск ф/с 13-частота ф/с 14-перепад 15-вставка
        self.FRej = array.array(uint16, [0] )
    #   quint32 FKolTN; //(default: 65538) Количество тест-наборов +2
        self.FKolTN = array.array(uint32, [0] )
    #   quint8 FKolKan; //(default:146) Количество каналов +2
        self.FKolKan = array.array(uint8, [0] )
    #   TCycleEvensData FCyc[8];  // циклы (не более 8)
        self.FCyc = [TCycleEvensData() for i in xrange(8)]
    #   quint8 FRezerv[5];       // резерв
        self.FRezerv = array.array(uint8, [0 for i in xrange(5)] )
    #   quint8 FMsOst[MAXNumber16]; // точки останова 1-стоп, 2- конец,3- вставка, 4-цикл, 5-метка
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
        self.lk.LKData.FRej[0] = 0x88CA;
        self.lk.LKData.FKolTN[0] = 65538;
        self.lk.LKData.FKolKan[0] = 146;        

    def store_params(self, *params):
        channels = {}
        for p in params:
            for ch in p.ch:
                if ch not in channels:
                    channels[ch] = p
                else:
                    raise AssertionError( "Duplicate channel {0} in parameter {1}. Already defined in {2} param.".format(ch, p.name, channells[ch].name) )
        sorted_channels = sorted([key for key in channels], key = lambda i: i)
        max_len = max( [len(p) for p in params ] )
        if max_len > MAXNumber16:
            max_len = MAXNumber16
        for p in params:
            p.expand(max_len)
        for ch in sorted_channels:
            for tn in xrange(max_len):
                d_bit = get_bit(channels[ch][tn][0], channels[ch].nbit(ch))
                self.lk.MassData[ch/16].FMsTs[tn] |= d_bit << (ch%16)

                io_bit = 1 if channels[ch][tn][2] == IN else 0
                self.lk.MassData[ch/16].FMsKm[tn] |= io_bit << (ch%16)

                m_bit = get_bit(channels[ch][tn][1].mask, channels[ch].nbit(ch))
                self.lk.MassData[ch/16].FMsMk[tn] |= m_bit << (ch%16)

        position = 0
        ch_list_in_all_param = []
        for p in params:
            for ch in p.ch:
                ch_list_in_all_param.append(ch)

        for ch in ch_list_in_all_param:
            self.lk.MassData[position/16].FMskan[position % 16] = ch
            position = position + 1
            name = channels[ch].name[:8] + "_" + str(channels[ch].nbit(ch)) if channels[ch].n_ch > 1 else channels[ch].name
            name = struct.pack("11p", name)
            name = array.array(uint8, name)
            for i, char in enumerate(name):
                self.lk.MassData[ch/16].FMspin[ (ch%16)*11 + i ] = char
        
        used_ch = set(ch_list_in_all_param)
        all_ch = set(xrange(144))
        unused_ch = all_ch - used_ch

        for ch in unused_ch:
            self.lk.MassData[position/16].FMskan[position % 16] = ch
            position = position + 1

        self.lk.LKData.FKolTN[0] = max_len + 2

    def write(self, filename):
        # @type filename: string
        with open( filename, "wb") as f:
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

def end():
    lk = sps_lk()
    list = [p[i] for i in p]
    lk.store_params(*list)
    lk.write(PROGRAM_NAME+".lk")
