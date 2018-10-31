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
    url = "https://wenku.baidu.com/search?word={}&lm=3&od=0&page=search&sort_type=0&type=sort_click&org=0".format(text)
    #log文件名称
    logfile = "log{}.txt".format(time.strftime('%Y%m%d%H%M',time.localtime(time.time())))
        
    def logit(self,content):
        with open(self.logfile,'a') as f:
            f.write(content+'\n')
            print(content)
            
    def start_requests(self):
        yield scrapy.Request(url = self.url,callback = self.ParseResult)
        pass
    
    def ParseResult(self,response):
    
        sign = response.css('div#xs-task h2.tip::text').extract_first()
        if sign is not None and sign == '没有找到满意的文档?':
            self.logit('没有找到:{}'.format(self.text))
            self.close()
        
        #获取搜索结果中的的ppt地址
        urls = response.css('span[title="ppt"]+a::attr(href)').extract()
        filenames= response.css('span[title="ppt"]+a::attr(title)').extract()
        cur_page = response.css('div.page-content span[class~=cur ]::text').extract_first()
        self.logit("爬取第{}页".format(cur_page))
        
        for u in urls:
            if self.text in filenames[urls.index(u)]:
                yield scrapy.Request(url=u,callback=self.pptParse,meta={"curpage":cur_page})
        
        #测试用,每页只爬取第一条
        #yield scrapy.Request(url=urls[0],callback=self.pptParse,meta={"curpage":cur_page})
        
        #获取下一页的地址        
        next_page = response.css('a.next::attr(href)').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(url=next_page,callback=self.ParseResult)
        else:
            self.logit('没有更多页')
            
    
    #创建文件夹函数
    def mkdir(self,name):
        try:
            os.mkdir('./{}'.format(name))
            return True
        except FileExistsError:
            return False
    #保存图片，接受文件夹名，和图片编号
    def savePic(self,url,filename,count):
        filepath='./{}/{}.jpg'.format(filename,count)
        urllib.request.urlretrieve(url,filepath)
        count+=1
        print('保存了{:0>3}张图'.format(count),end='\r')
        return count
    
    def pptParse(self,response):
        item = WenkupptItem()
        cur_page = response.meta['curpage']
        item['docTittle'] = response.css('span#doc-tittle-2::text').extract()
        item['docTittle'] =''.join(item['docTittle'] )
        item['docTittle'] = cur_page + '-' + item['docTittle']
        item['img_urls'] = response.css('div.ppt-image-wrap img::attr(src)').extract()
        item['img_hidden_urls']=response.css('div.ppt-image-wrap img::attr(data-src)').extract()

        #获取ppt页面的左上角block
        payPPT= response.css('div[style="display: block;"] i.triangle-left+span::text').extract_first() == "付费文档"
        #如果该文件是付费文档，则不进行下载
        if payPPT ==True:
            self.logit("付费文档url：{}".format(response.url))
            return print("付费文档：{}".format(item['docTittle']))
 
        if item['img_urls'] is not None: 
            count = 1
            filecount=0
            filename = item['docTittle']
            while self.mkdir(filename) == False:
                filecount+=1
                filename=item['docTittle']+str(filecount)
                pass
            self.logit('文件地址：{}\n图片地址数量{},保存至文件夹:{}'\
                  .format(response.url,\
                          len(item['img_urls'])+len(item['img_hidden_urls']),\
                          filename))
            
            for url in item['img_urls']:
                count = self.savePic(url,filename,count)
            for url in item['img_hidden_urls']:
                count = self.savePic(url,filename,count)

    
        