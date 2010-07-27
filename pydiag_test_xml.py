#!/usr/bin/python
# -*- coding: windows-1251 -*-

from pydiag import *
import xml.dom as xml

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