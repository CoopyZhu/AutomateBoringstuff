# -*- coding: utf-8 -*-
"""
Created on Mon Nov 20 21:11:14 2017
将文件按照科室名移动至相应文件夹
@author: Coopy
"""

import os,shutil

def getfilelist():
    rawlist = os.listdir()
    filelist = []
    for f in rawlist:
        if f.endswith('docx'):
            filelist.append(f)
    return filelist


def getdir(ksname):
    rootdir = os.getcwd()
    todir = None
    for folderName,subfolders,filenames in os.walk(rootdir):
        if folderName.endswith(ksname):
            todir = folderName
            break
    if todir == None:
        print('找不到该科室')
    return todir

def movefile(file,todir):
    try:
        shutil.move(file,todir)
        print('将文件【{}】\n移动至【{}】'.format(file,todir))
    except Exception as err:
        print('发生错误{}'.format(err))

def getksname(file):
    splited = file.split('-')
    ksname = splited[-2]
    return ksname
    


def main():
    input('''请确保该文件与各科室文件夹位于同一目录，
需要移动的docx文件与该文件并列
命名方式：表名-文件夹名-YYYYMM
输入任意键继续''')
    filelist = getfilelist()
    for file in filelist:
        ksname = getksname(file)
        todir = getdir(ksname)
        movefile(file,todir)

main()