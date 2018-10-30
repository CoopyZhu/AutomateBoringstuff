# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import scrapy 
from scrapy.pipelines.images import ImagesPipeline


class WenkupptPipeline(object):
    def process_item(self, item, spider):
        return item

class ImagesPipline(ImagesPipeline):
    def get_media_requests(self,item,info):
        for url in item['img_urls']:
            yield scrapy.Request(url)
            
    #重写item_completed方法
    #def item_complete(self, results, item, info):
     #   image_path = [x["path"] for ok, x in results if ok]
        
'''   
    def item_completed(self, results, item, info):
        file_paths = 
'''