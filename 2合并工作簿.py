# -*- coding: utf-8 -*-
"""
Created on Mon Nov 20 11:58:06 2017


合并多工作表的列
@author: Coopy
"""

from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl import Workbook
import re,os
import pandas as pd


#pattern = re.compile(r'd+.xlsx')


def getpathlist():
    y = ''
    while not y == 'y':
        y = input('请确保该脚本所处目录下仅包括需要合并的excel文件，\n继续请输入y')
    rootdir = os.getcwd()
    path_list = []
    
    
    for parent, dirnames,filenames in os.walk(rootdir):
        for fn in filenames:
            if 'xlsx' in fn:
                path_list.append(os.path.join(parent,fn))
    return path_list

def getdf(path):
    df2 = pd.read_excel(path)

    return df2

def mergedf(df0, df2):
    #按照第一列排序
    df2 = df2.sort_values(df2.columns[0])
    
    #合并
    df1 = pd.concat([df0,df2],axis=1)
    
    return df1

def tows(df):
    wb = Workbook()
    ws = wb.active

    for r in dataframe_to_rows(df, index=True, header=True):
        ws.append(r)
    return wb,ws

def mergedate(ws):
    length = len(tuple(ws.columns))
    for c in range(2,length+1,6):
        ws.merge_cells(start_column = c, end_column = c+5,start_row = 1,end_row = 1)
    
    

def main():
    pathlist = getpathlist()
    df0 = pd.read_excel(pathlist[0])
    df0 = df0.sort_values(df0.columns[0])
    for path in pathlist[1:]:
        df2 = getdf(path)
        df0 = mergedf(df0,df2)
    wb,ws = tows(df0)
    mergedate(ws)
    wb.save('合并后.xlsx')
    
main()