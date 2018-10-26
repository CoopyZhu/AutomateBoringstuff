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
        tags=response.css('ul.tags-list a[style]')
        item = Mingyan2Item()
        for tag in tags:
            item["tag_urls"]=tag.css('::attr(href)').extract_first()
            item["tag_name"]=tag.css('::text').extract_first().strip()
            self.log(item["tag_name"])
            yield scrapy.Request(item["tag_urls"],callback=self.parse_mingyan,meta=item)
            
            
    def parse_mingyan(self,response):
        item=response.meta
        self.log('item.keys{}'.format(item.keys))
        mingyan1 = response.css('div[class="quote post"]')
        tag = item["tag_name"]
        filename = tag+".txt"
        for m in mingyan1:
            text = m.css('.text::text').extract_first()
            author = m.css('span small::text').extract_first()
            with open(filename,"a+") as f:
                f.write("内容：{}\n作者：{}\n标签:{}\n".format(text,author,tag)) 
        self.log("保存文件：{}".format(filename)) #记录日志
        next_page= response.xpath('//li[@class="next"]//@href').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse_mingyan,meta=item)
        mingyantags.count+=1