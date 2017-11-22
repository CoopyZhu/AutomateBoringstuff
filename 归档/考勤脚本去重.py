#! python3
考勤脚本，去重
# -*- coding: utf-8 -*- 
import os, pprint, re, openpyxl
import pandas as pd
from pandas import DataFrame
import pprint

input('请将各月份文件夹与该脚本放置于同目录下\n输入任意键继续')

rootdir = os.getcwd()

filelist=[] 
fns=[]
for parent, dirnames,filenames in os.walk(rootdir):
    for fn in filenames:
        if '$' in fn:   
            pass
        elif fn.endswith('.xls') or fn.endswith('.xlsx'): 
            fns.append(fn)
            filelist.append(os.path.join(parent,fn))
fns.append('总计')
fns.append(str(len(fns)-1))

fnsfile = open(rootdir +'\\读取的文件名.txt','w')
fnsfile.write(pprint.pformat(fns))
fnsfile.close()


reg = re.compile(r'(\d+月)+')

alldic={}


for f in filelist:
    print('正在处理:',os.path.basename(f))
    sheet = pd.read_excel(str(f))
    data = sheet.loc[:,['证件编号','姓名','备注']]
    for i in data.index:  
        d_id = str(data.loc[i]['证件编号'])
        d_name = data.loc[i]['姓名']
        d_note = data.loc[i]['备注']
        d_checkdate = re.findall(reg,d_note)
        str_check = ''.join(d_checkdate)
        try:
            alldic[d_id] += str_check
        except:
            alldic[d_id] = str_check
          

mywb = openpyxl.Workbook()
mysheet = mywb.get_sheet_by_name('Sheet')
i=1
for key in alldic.keys():
    An = 'A'+str(i)
    Bn = 'B'+str(i)
    mysheet[An] = str(key)
    alldic[key]=[i for i in set(alldic[key].split('月'))]
    alldic[key].remove('')
    alldic[key]='月'.join(alldic[key])
    alldic[key] +='月'
    mysheet[Bn] = alldic[key]
    i+=1
mywb.save(rootdir+'\\$考勤统计结果.xlsx')
print('已将结果保存至  $考勤统计结果.xlsx')