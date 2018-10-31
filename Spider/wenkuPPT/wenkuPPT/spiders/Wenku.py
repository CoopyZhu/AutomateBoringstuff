# -*- coding: utf-8 -*-
"""
Created on Tue Oct 30 16:25:51 2018

@author: 朱诚锐
"""

import scrapy
from wenkuPPT.items import WenkupptItem
import urllib
import os
import time

class SearchPPTSpider(scrapy.Spider):
    name = "downloadppt"
    text = input("请输入要搜索的ppt关键字，并猛敲回车\n")
    #检索文库ppt内容的url固定格式
    url = "https://wenku.baidu.com/search?word={}&lm=3&od=0&page=search&sort_type=0&type=sort_click&org=0".format(text)
    #log文件名称
    logfile = "log{}.txt".format(time.strftime('%Y%m%d%H%M',time.localtime(time.time()))) 
    
    def logit(self,content):
        '''
        将内容写入logfile，并print
        '''
        with open(self.logfile,'a') as f:
            f.write(content+'\n')
            print(content)
            
    def start_requests(self):
        yield scrapy.Request(url = self.url,callback = self.ParseResult)
        pass
    
    #处理搜索结果页
    def ParseResult(self,response):
        #获取搜索结果不存在的提示，若存在，结束爬虫
        sign = response.css('div#xs-task h2.tip::text').extract_first()
        if sign is not None and sign == '没有找到满意的文档?':
            self.logit('没有找到:{}'.format(self.text))
            self.close()
        
        #获取搜索结果中的的ppt地址
        urls = response.css('span[title="ppt"]+a::attr(href)').extract()
        filenames= response.css('span[title="ppt"]+a::attr(title)').extract()
        cur_page = response.css('div.page-content span[class~=cur ]::text').extract_first()
        self.logit("爬取第{}页".format(cur_page))
        #将ppt地址堆入请求
        for u in urls:
            #确保关键字在文件名中
            if self.text in filenames[urls.index(u)]:
                yield scrapy.Request(url=u,callback=self.pptParse,meta={"curpage":cur_page})
        
        #测试用,每页只爬取第一条
        #yield scrapy.Request(url=urls[0],callback=self.pptParse,meta={"curpage":cur_page})
        
        #获取下一页的地址        
        next_page = response.css('a.next::attr(href)').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)#链接地址
            yield scrapy.Request(url=next_page,callback=self.ParseResult)
        else:
            self.logit('没有更多页')
            
    
    #创建文件夹，若文件夹已存在，返回False
    def mkdir(self,name):
        try:
            os.mkdir('./{}'.format(name))
            return True
        except FileExistsError:
            return False
    #使用urllib保存图片，接受文件夹名，和图片编号
    def savePic(self,url,filename,count):
        filepath='./{}/{}.jpg'.format(filename,count)
        urllib.request.urlretrieve(url,filepath)
        count+=1
        print('保存了{:0>3}张图'.format(count),end='\r')
        return count
    
    #处理ppt页
    def pptParse(self,response):
        item = WenkupptItem()
        #当前页号
        cur_page = response.meta['curpage']
        #ppt名称
        item['docTittle'] = response.css('span#doc-tittle-2::text').extract()
        item['docTittle'] =''.join(item['docTittle'] )#防止名称标红，需要链接一次
        item['docTittle'] = cur_page + '-' + item['docTittle']#将所属页码名称作为前缀
        #图片地址
        item['img_urls'] = response.css(
            'div.ppt-image-wrap img::attr(src),'+
            'div.ppt-image-wrap img::attr(data-src)').extract()
        
        #获取ppt页面的左上角block
        payPPT= response.css('div[style="display: block;"] i.triangle-left+span::text').extract_first() == "付费文档"
        #如果该文件是付费文档，则不进行下载
        if payPPT ==True:
            self.logit("付费文档url：{}".format(response.url))
            return print("付费文档：{}".format(item['docTittle']))
 
        if item['img_urls'] is not None: 
            count = 1
            filecount=0
            #文件夹名称=ppt名称
            filename = item['docTittle']
            #若文件夹已存在，在其后添加序号
            while self.mkdir(filename) == False:
                filecount+=1
                filename=item['docTittle']+str(filecount)
                pass
            self.logit('文件地址：{}\n图片地址数量{},保存至文件夹:{}'\
                  .format(response.url,\
                          len(item['img_urls']), filename))
            #保存图片地址内容
            for url in item['img_urls']:
                count = self.savePic(url,filename,count)


    
        