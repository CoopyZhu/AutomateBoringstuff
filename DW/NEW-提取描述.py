# -*- coding: utf-8 -*-
"""
Created on Wed Oct 10 17:04:54 2018

@author: 朱诚锐
"""
import jieba
import jieba.posseg as pseg
import re

def ParseRawDescribe(RawContent):
    result = pseg.cut(RawContent, HMM=False)
    r_list = []
    #将分词结果存为list[[word,flag],]
    for w in result:
        r_list.append([w.word,w.flag])
    outp = []#由切片组成，短语的slic表示
    slic = []#由jieba分词结果组成
    for i in range(len(r_list)):
        w = r_list[i]
        w_before = r_list[i-1]
        #如果该词是 解剖 或 位置，对其前置词进行分析
        if w[1] in ["jp","wz"]:
            #如果前置词是标点（除顿号）、位置词，则对slic进行终结
            if w_before[1] in ["wz","jp","blgx"] or w_before[0]=="、"
            #若前置词是其他，则将slic移入outp，重新开始
            if w_before[1]  not in ["x","wz"] or w_before[0]=="、":
                slic.append(w)
            else:
                outp.append(slic)
                slic = []
                slic.append(w)
        else:
            slic.append(w)
    #End Slic
    outp.append(slic)
