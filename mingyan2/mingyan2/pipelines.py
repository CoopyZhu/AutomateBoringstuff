# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exceptions import DropItem

#去重过滤器
class Mingyan2Pipeline(object):
    def __init__(self):
        self.ids_seen = set()


    def process_item(self, item, spider):
        if item['id'] in self.ids_seen:
            raise DropItem('Duplicate item found {s}'.format(item))
        else:
            self.ids_seen.add(item)
            return item

    def open_sipder(self,spider):
        pass
    
    def close_spider(self,spider):
        pass