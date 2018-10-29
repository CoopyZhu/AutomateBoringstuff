# -*- coding: utf-8 -*-
"""
使用selenium调用headless Chrome，未配置环境时需要引用绝对地址

@author: 朱诚锐
"""

from selenium import webdriver
from scrapy.http import HtmlResponse
from selenium.webdriver.chrome.options import Options
import time

#滚动至页面底部的js
js="""
function scrollToBottom() {

    var Height = document.body.clientHeight,  //文本高度
        screenHeight = window.innerHeight,  //屏幕高度
        INTERVAL = 100,  // 滚动动作之间的间隔时间
        delta = 500,  //每次滚动距离
        curScrollTop = 0;    //当前window.scrollTop 值

    var scroll = function () {
        curScrollTop = document.body.scrollTop;
        window.scrollTo(0,curScrollTop + delta);
    };

    var timer = setInterval(function () {
        var curHeight = curScrollTop + screenHeight;
        if (curHeight >= Height){   //滚动到页面底部时，结束滚动
            clearInterval(timer);
        }
        scroll();
    }, INTERVAL)
}
    scrollToBottom
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
            driver.excute_script(js) #可执行js，模仿用户操作，该实例为将页面拉至最底端
            time.sleep(3)#等待执行JS
            # 可使用selenium 自带的wait，参照 https://selenium-python-zh.readthedocs.io/en/latest/waits.html
            body = driver.page_source
            print("访问："+request.url)
            return HtmlResponse(driver.current_url, body=body, encoding="utf-8",request=request)
        else:
            return None