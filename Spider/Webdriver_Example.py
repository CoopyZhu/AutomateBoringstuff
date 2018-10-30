# -*- coding: utf-8 -*-
"""
使用selenium调用headless Chrome，未配置环境时需要引用绝对地址

@author: 朱诚锐
"""

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
        if(curScrollTop>=TextTop){clearInterval(timer)} //若实际位置等于文本最大高度，清除间隔函数
        else{scroll()}},interval)
            }
     scrollToBottom()

"""

class JavaScriptMiddleware(object):
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