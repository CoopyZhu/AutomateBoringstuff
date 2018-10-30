# -*- coding: utf-8 -*-
"""
Created on Tue Oct 30 17:36:44 2018

@author: 朱诚锐
"""

import scrapy
from wenkuPPT.items import WenkupptItem
import urllib
import os

class SearchPPTSpider(scrapy.Spider):
    name = "down1ppt"
 
    
    def start_requests(self):
        u = "https://wenku.baidu.com/view/5d8b29bf2f60ddccdb38a072.html?from=search"
        yield scrapy.Request(url = u,callback = self.pptParse)
        pass
    
    def ParseResult(self,response):
        sign = response.css('div#xs-task h2.tip::text').extract_firts()
        if sign == '没有找到满意的文档?':
            self.close()
        #获取搜索结果的ppt地址
        urls = response.css('p.fl a::attr(href)').extract()
        for u in urls:
            yield scrapy.Request(url=u,callback=self.pptParse)
            pass
        #获取下一页的地址
        next_page = response.css('a.last::attr(href)').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(url=next_page,callback=self.ParseResult)
        pass
    
    def pptParse(self,response):
        item = WenkupptItem()
        item['docTittle'] = response.css('span#doc-tittle-2::text').extract()
        item['docTittle'] =''.join(item['docTittle'] )
        item['img_urls'] = response.css('div.ppt-image-wrap img::attr(src)').extract()
        item['img_hidden_urls']=response.css('div.ppt-image-wrap img::attr(data-src)').extract()
        print('url地址数量{},保存至文件夹{}'.format(len(item['img_urls'])+len(item['img_hidden_urls']),item['docTittle']))
        count = 1
        try:
            os.mkdir('./{}'.format(item['docTittle']))
        except:
            pass
        for url in item['img_urls']:
            filename='./{}/{}.jpg'.format(item['docTittle'],count)
            urllib.request.urlretrieve(url,filename)
            count+=1
            print('保存了{}张图'.format(count))
            pass
        for url in item['img_hidden_urls']:
            filename='./{}/{}.jpg'.format(item['docTittle'],count)
            urllib.request.urlretrieve(url,filename)
            count+=1
            print('保存了{}张图'.format(count))
      
        yield item