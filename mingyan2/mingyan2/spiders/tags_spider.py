# -*- coding: utf-8 -*-
"""
Created on Thu Oct 25 15:09:20 2018

@author: 朱诚锐
"""

import scrapy
from mingyan2.items import Mingyan2Item
import re

class mingyantags(scrapy.Spider):
    name= 'mingyantag'
    start_urls=["http://lab.scrapyd.cn/",
            ]
    ttags=[]
    count = 0
    
    def parse(self,response):
        tags=response.xpath('//ul[@class="tags-list"]//a[@style]')
        for tag in tags:
            Mingyan2Item.tag_urls=tag.xpath('@href').extract_first()
            Mingyan2Item.tag_name=tag.xpath('text()').extract_first()
            self.log(Mingyan2Item.tag_name)
            mingyantags.ttags.append(Mingyan2Item.tag_name.strip())
            yield scrapy.Request(Mingyan2Item.tag_urls,callback=self.parse_mingyan)
            
            
    def parse_mingyan(self,response):
        mingyan1 = response.xpath('//div[@class="quote post"]')
        tag = response.xpath('//head//meta[@name="keywords"]/@content')[1].extract()
        filename = tag+".txt"
        for m in mingyan1:
            text = m.xpath('.//span[@class="text"]/text()').extract_first()
            author = m.xpath('.//span/small/text()').extract_first()
            with open(filename,"a+") as f:
                f.write("内容：{}\n作者：{}\n标签:{}\n".format(text,author,tag)) 
        self.log("保存文件：{}".format(filename)) #记录日志
        next_page= response.xpath('//li[@class="next"]//@href').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse_mingyan)
        mingyantags.count+=1