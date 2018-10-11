# -*- coding: utf-8 -*-
"""
Created on Wed Oct 10 17:04:54 2018

@author: 朱诚锐
"""
import jieba
import jieba.posseg as pseg
import re
from openpyxl import load_workbook

jieba.load_userdict(r"User_Dict.txt")


def Cut_byAnatomy(Content):
    '''
    将描述原文根据解剖位置切分成段落
    判断
    一个set为（、）（并列关系）（位置词）解剖部位     
    识别解剖部位，若其前面不是顿号、位置词或解剖部位，则进行分段
    '''
    if not isinstance(Content,str):
        raise TypeError("not string type")
    Content = Content.replace(" ","")
    outp = []#由切片组成，短语的slic表示
    slic = ""#由jieba分词结果组成
    
    result = pseg.cut(Content, HMM=False)
    r_list = []
    #将分词结果存为list[[word,flag],]
    for w in result:
        r_list.append([w.word,w.flag])
    
    for i in range(len(r_list)):
        w = r_list[i]
        w_before = r_list[i-1]
        try:
            w_after = r_list[i+1]
        except:
            w_after = ["",""]
        if i==0:
            w_before=["",""]
        #如果该词是 解剖 或 位置，对其前置词进行分析
        if w[1] in ["jp"]:
            #若其前面不是顿号、位置词或解剖部位，则将slic移入outp，从该词新建slic
            if (w_before[1] not in ["jp","wz","blgx"]) and w_before[0] not in["、","-"]:
                outp.append(slic)
                slic = w[0]
            else:
                slic += w[0]
        elif w[1] in ["wz"]:
            if w_after[1] not in ['jp',"wz","blgx"]:
                slic += w[0]
            else:
                if (w_before[1] not in ["jp","wz","blgx"]) and w_before[0] not in["、","-"]:
                    outp.append(slic)
                    slic=w[0]
                else:
                    slic +=w[0]               
        else:
            slic+= w[0]
    #End Slic
    outp.append(slic)
    while "" in outp:
        outp.remove("")
            
        return outp

def Cut_byXHMC(Text):
    '''
    处理的结果，提取其中的信号描述
    '''
    result = pseg.cut(Text,HMM=False)
    #将flag和word分别存为list
    flags = []
    words = []
    for w in result:
        flags.append(w.flag)
        words.append(w.word)
    if "xhmc" in flags:
        pass
    
def WriteToCell(Cell,Value,quto="、"):
    """
    将内容写入单元格，去重，中间用quto分隔
    """
    if Cell.value ==None or Cell.value =="":
        Cell.value = Value
    else:
        if Value not in Cell.value:
            Cell.value += (quto+Value)

'''
czxf[....]增强
'''

    
def main():
    path = r"C:\Users\朱诚锐\OneDrive\DEEPWISE\问诊平台\数据\征象提取"
    #文件名
    filename = r"\z-脑膜瘤100（病理确认）--接收时间1008--整理中。。。.xlsx"
    dirc = path+filename
    
    book = load_workbook(dirc)
    sheet = book["Sheet1"]
    content_col=9
    raw_content_col = 7
    diagnosis_col = 8
    jp_col = 10
    xhxz_col = 24
    zqsm_col = 16
    zqsmlx_col = 17
    zw_col = 27
    disease="脑膜瘤"
    #遍历数据行,
    for row in range(2,sheet.max_row+1):
        
        diagnosis = sheet.cell(row=row,column=diagnosis_col).value.split('\n')
        content_cell = sheet.cell(row=row,column=content_col)
        raw_content = sheet.cell(row=row,column=raw_content_col).value
        xhxz_cell = sheet.cell(row=row,column=xhxz_col)
        zqsm_cell = sheet.cell(row=row,column=zqsm_col)
        jp_cell = sheet.cell(row=row,column=jp_col)
        zw_cell = sheet.cell(row=row,column=zw_col)
        print("row:{}\nraw_content:{}\n{}".format(row,raw_content,"-"*60))
        '''
        将发病位置提出
        '''
        for each_dig in diagnosis:
            if disease in each_dig:
                if "占位" in each_dig:
                    zw_cell.value = "占位"
                result = pseg.cut(each_dig,HMM=False)
                for w in result:
                    if w.flag == "jp":
                        WriteToCell(jp_cell,w.word,"。")
        
        '''
        将疾病部位所在的段落提取出
       
        '''
        try:
            jp = jp_cell.value.split("、")
            print("jp:",jp)
            for each_jp in jp:
                for sentence in (Cut_byAnatomy(raw_content)):
                    if each_jp in sentence:
                        WriteToCell(content_cell,sentence)
        except:
            content_cell.value = raw_content

        
        content = sheet.cell(row=row,column=content_col).value
        print("content:",content)
        if content == None:
            continue
        #根据标点符号拆分内容
        contents = re.split(r",|，|。|、|;|；",content)
        for cont in contents:
            #print("content:",cont)
            result = pseg.cut(cont,HMM=False)
            flags=[]
            words=[]
            for w in result:
                flags.append(w.flag)
                words.append(w.word)
            
            try:
                #对增强扫描进行处理
                if "zqsm" in flags:
                    #print("flags:{} \nwords:{}".format(flags,words))
                    #如果存在zqsm，同时有存在性负的提示词，则记为不强化
                    if "czxf" in flags and "xhmc" not in flags:
                        WriteToCell(zqsm_cell,"不强化")
                    elif "czxz" in flags and"czxf" not in flags:
                        WriteToCell(zqsm_cell,words[flags.index("czxz")]+"强化")
                #对信号形状进行处理：如果信号形状和解剖或信号名称同时出现
                elif "xhxz" in flags and ("jp" in flags or "xhmc" in flags):
                    WriteToCell(xhxz_cell,words[flags.index("xhxz")])
                #对信号进行提取
            except:
                continue
        temp = input()
    #保存
    book.save(path+"\z-python处理后.xlsx")

main()