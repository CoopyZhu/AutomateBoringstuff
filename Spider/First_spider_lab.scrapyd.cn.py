# -*- coding: utf-8 -*-
"""
Created on Thu Oct 25 12:16:53 2018

@author: 朱诚锐
"""

import scrapy

class mingyan(scrapy.Spider):
    name = "mingyan2"
    
    start_urls=[ #无需定义start_requests方法
            'http://lab.scrapyd.cn/page/1/',
            
            ]
    '''
    另一种初始链接写法
    def start_requests(self): #通过此方法爬取页面
        #爬取的链接
        urls=['http://lab.scrapyd.cn/page/1/',
              'http://lab.scrapyd.cn/page/2/',
              ]
        for url in urls:
            yield scrapy.Request(url=url,callback = self.parse)#将爬取到的页面提交给parse处理
    '''
    #使用start_urls必须定义parse方法
    def parse(self,response):
        filename = response.url.split('/')[-2]+".txt"
        
        mingyan1 = response.xpath('//div[@class="quote post"]')
        
        for m in mingyan1:
            
            text = m.xpath('.//span[@class="text"]/text()').extract_first()
            author = m.xpath('.//span/small[@class="author"]/text()').extract_first()
            tags = m.xpath('.//a[@class="tag"]/text()').extract()
            tags = ','.join(tags)
        
            with open(filename,"a+") as f:
                f.write("内容：{}\n作者：{}\n标签：{}\n\n".format(text,author,tags))
        self.log("保存文件：{}".format(filename)) #记录日志
        
        next_page= response.xpath('//li[@class="next"]//@href').extract_first() #提取下一页的链接
        
        if next_page is not None:
            
            """
             如果是相对路径，如：/page/1
             urljoin能替我们转换为绝对路径，也就是加上我们的域名
             最终next_page为：http://lab.scrapyd.cn/page/2/        
            """
            next_page = response.urljoin(next_page)
            
            """
            接下来就是爬取下一页或是内容页的秘诀所在：
            scrapy给我们提供了这么一个方法：scrapy.Request()
            这个方法还有许多参数，后面我们慢慢说，这里我们只使用了两个参数
            一个是：我们继续爬取的链接（next_page），这里是下一页链接，当然也可以是内容页
            另一个是：我们要把链接提交给哪一个函数(callback=self.parse)爬取，这里是parse函数，也就是本函数
            当然，我们也可以在下面另写一个函数，比如：内容页，专门处理内容页的数据
            经过这么一个函数，下一页链接又提交给了parse，那就可以不断的爬取了，直到不存在下一页

            """

            yield scrapy.Request(next_page, callback=self.parse)
        