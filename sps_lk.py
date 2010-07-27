#!/usr/bin/python
# -*- coding: windows-1251 -*-

from pydiag import *
import struct
import array

"""
const int MAXNumber16 = 0x10000;
const int CountPlats = 9;


/*
Для достижения унификации запись имеет переменные составляющие, а именно:
Глубина тестовых-наборов(ТН) в  комплексах этого типа 16бит
(т.е. MAXNumber16=$FFFF)
Логическое число канальных плат начиная с 0 (лог. плата содержит 16 каналов,
независимо от реализации  модуля каналов)  для Скворец-М
(144кан - CountPlats=8),Скворец-МН(96кан - CountPlats=5)
*/



 // инфа о циклах
struct TCycleEvensData
{
   quint32 fTn0;   // нач. ТН
   quint32 fLength; // глубина цикла
   quint16 fCount; // кол-во повторений // 1 - бесконечность
   quint16 fDiff; // перепад (побитно: 15-14 - 00-нет/ 01 - 0/ 10 - 1/ 11 - по 0 и по 1
                 // (не исп.)// 13-0 - номер канала перепада)
};

// Общие данные
struct ToffsenData16
{
    quint8 SRea;  //(default: $E1)
    quint16 FRej;  // (default: $88CA) параметры режима (побитно): 0-внеш 1-брак ур. 2-шаг 3 брак фун. 4-цикл 5-удерж.ур. 6-стоп 7-конец 8-11-частота 12-запуск ф/с 13-частота ф/с 14-перепад 15-вставка
    quint32 FKolTN; //(default: 65538) Количество тест-наборов +2
    quint8 FKolKan; //(default:146) Количество каналов +2
    TCycleEvensData FCyc[8];  // циклы (не более 8)
    quint8 FRezerv[5];       // резерв
    quint8 FMsOst[MAXNumber16]; // точки останова 1-стоп, 2- конец,3- вставка, 4-цикл, 5-метка
};

// Запись Univer16
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
        self.FMsTsFMsKm = array.array(uint16, [0 for i in xrange(MAXNumber16)] )
    #   quint16 FMsMk[MAXNumber16];  // массив маски(выкл /вкл)
        self.FMsTsFMsMk = array.array(uint16, [0 for i in xrange(MAXNumber16)] )
    #   quint8 FMskan[16]; // соответствие номеров каналов строкам при перетаскивании (default: 0 – 143 или 0 - 95)
        self.FMsTsFMskan = array.array(uint8, [0 for i in xrange(16)] )
    #   quint8 FMspin[16][11];  // название контактов (примечание) (default:’’)
        self.FMsTsFMspin = array.array(uint8, [0 for i in xrange(16*11)] )
    #   quint8 FMsUrov[16][3];  // 0-уровни 0    1- уровни 1   2-ур.компаратора (default: [x,0]:=$80; [x,1]:=$5D; [x,2]:=$76;)
        self.FMsTsFMsUrov = array.array(uint8, [0 for i in xrange(16*3)] )
    #   quint16 FMskk;         // отображение каналов (побитовое  выкл/вкл ) (default: $FFFF)
        self.FMsTsFMskk = array.array(uint16, [0] )
    #   quint16 FAdv[16];  //зарезервированный (default: $0000)
        self.FMsTsFAdv = array.array(uint16, [0 for i in xrange(16)] )

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

    def write(self, filename):
        # @type filename: string
        with open("w", filename) as f:
            for MassData_i in self.lk.MassData:
                # @type MassData_i: TMassData16
                # @todo: write
                pass

            
    
    
#// Общие данные
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

        #Добавляем комментарии если они есть
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