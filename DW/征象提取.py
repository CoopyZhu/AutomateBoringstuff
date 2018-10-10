# -*- coding: utf-8 -*-
"""
Created on Mon Oct  8 15:15:44 2018

@author: 朱诚锐

提取信息
"""
import jieba
import jieba.posseg as pseg
from openpyxl import load_workbook
import re
#载入自定义词典
jieba.load_userdict("User_Dict.txt")
#文件路径
path = r"C:\Users\朱诚锐\OneDrive\DEEPWISE\问诊平台\数据\征象提取"
#文件名
filename = r"\z-少突星形细胞瘤20LL.xlsx"
dirc = path+filename

book = load_workbook(dirc)
sheet = book["Sheet1"]

#提取疾病部位

#遍历数据行
for row in range(2,sheet.max_row+1):
    #获取改行疾病名称
    name = "瘤"
    #获取诊断内容，分行，存为list
    diagonse = sheet.cell(row=row,column=5).value.split("\n")
    #获取描述内容，分行，存为list
    describe = sheet.cell(row=row,column=4).value.split("\n")
    #初始化提取后的描述和诊断
    p_describe=""
    p_diagnose=""
    
    #遍历诊断list
    for x in diagonse:
        #若该内容中出现目标疾病名称
        if name in x:
            #存为提取后的诊断
            p_diagnose = x
            break #跳出循环
        else:
            pass
        
    #对该诊断进行分词
    result = pseg.cut(p_diagnose)
    #遍历分词后的结果
    for w in result:
        #若该词的词性为jp
        if w.flag=="jp":
            print("row:",row,w.word,"\\",w.flag)   #打印该词\词性
            #遍历描述list
            for des in describe:
                #若该解剖部位存在
                if w.word in des:
                    #存为提取后的描述
                    p_describe = des
                    break #跳出循环
                else:
                    pass
            #若描述中未找到目标部位，则将全部文本存入提取后的描述
            if p_describe =="":
                p_describe = "\n".join(describe)
            break
        #若未找到含词性为jp词语的语句，则跳过
        else:
            pass
    #将结果保存至excel中
    sheet.cell(row=row,column=6).value = p_describe
    sheet.cell(row=row,column=7).value = p_diagnose
    sheet.cell(row=row,column=8).value = w.word #部位
    
    
#提取信号
'''
def WriteTo(w,row,result):
    if w.flag=="xhmc":
        xhmc = ["T1WI","T2WI","FLAIR","DWI","","","","ADC"]
        if w.word in xhmc:
            for ww in result:
                if ww.flag == "xhqd":
                    ww.word = ww.word +"信号"
                    existed_cell = sheet.cell(row=row,column=13+xhmc.index(w.word))
                    if existed_cell.value is None:
                        existed_cell.value=ww.word
                    else:
                        if ww.word in existed_cell.value:
                            next
                        else:
                            existed_cell.value =  existed_cell.value +"、" +ww.word
        

                            
#遍历每行内容                         
for row in range(2,sheet.max_row+1):
    text = sheet.cell(row=row,column=9).value
    if not text is None:
        #根据，。分隔为list
        describe = re.split(r"，|。|,",text)
        #遍历每句话
        for sentence in describe:
            print("sentence:",sentence)
            result = pseg.cut(sentence,HMM=False)
            #遍历该句中每个词
            for w in result:
                print("word:{} flag:{}".format(w.word,w.flag))
                #如果该句中有信号名称
                if w.flag =="xhmc":
                    #若该句中有顿号
                    sentences = sentence.split("、")
                    if "、"in sentence:
                        #遍历切分顿号后的每句
                        for sentence2 in sentences:
                            result2 = pseg.cut(sentence2,HMM=False)
                            for w2 in result2:
                                WriteTo(w2,row,result2)
                                continue
                            continue
                        break
                    else:
                        WriteTo(w,row,result)
                if w.flag =="xhxz":
                    existed_cell = sheet.cell(row=row,column=25)
                    if existed_cell.value is None:
                        existed_cell.value=w.word
                    else:
                        if w.word in existed_cell.value:
                            next
                        else:
                            existed_cell.value =  existed_cell.value +"、" +w.word
                
'''

#保存
book.save(path+"\z-少突星形细胞瘤20LL处理后.xlsx")
'''

'''