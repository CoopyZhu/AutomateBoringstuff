# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from selenium import webdriver
from scrapy.http import HtmlResponse
from selenium.webdriver.chrome.options import Options
import time



js="""
//适用于百度搜索结果页的窗体滚动，2018-1030
function scrollToBottom(){  
        interval = 1000; //移动间隔
        delta = 200; //每次移动的距离
        var scroll = function(){ //滚动函数
        var TextTop = document.body.clientHeight // 文本高度
        var docscrollTop = document.documentElement.scrollTop; //目前元素窗口位置
        var clientHeight = document.documentElement.clientHeight; //窗高
            window.scrollTo(0,docscrollTop+delta); //滚动
            };
        var timer = setInterval(function(){ //间隔函数
        var docscrollTop = document.documentElement.scrollTop; //目前元素窗口位置
        var clientHeight = document.documentElement.clientHeight; //窗高
        var curScrollTop= clientHeight + docscrollTop; //目前实际位置 = 窗高+元素窗口位置
        if(curScrollTop>=TextTop){clearInterval(timer)} //若实际位置等于文本最大高度，清楚间隔函数
        else{scroll()}},interval)
            }
     scrollToBottom()

"""

class HeadlessChromeMiddleware(object):
    def process_request(self, request,spider):
        if spider.name: #判断spider的名字
        # if request.meta.has_key("HeadlessChrome"):判断request的meta信息中是否含有对应字段
            print("Headless Chrome is starting....")
            chrome_options = Options()
            chrome_options.add_argument('--headless')
            driver_path=r"C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"
            driver = webdriver.Chrome(executable_path=driver_path,chrome_options=chrome_options)
            driver.get(request.url)
            time.sleep(1)
            #driver.execute_script(js) #可执行js，模仿用户操作，该实例为将页面拉至最底端
            time.sleep(3)#等待执行JS
            # 可使用selenium 自带的wait，参照 https://selenium-python-zh.readthedocs.io/en/latest/waits.html
            body = driver.page_source
            print("访问："+request.url)
            return HtmlResponse(driver.current_url, body=body, encoding="utf-8",request=request)
        else:
            return None




class Mingyan2SpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class Mingyan2DownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
