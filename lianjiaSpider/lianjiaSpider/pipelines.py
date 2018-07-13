# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from scrapy.conf import settings


class LianjiaspiderPipeline(object):
    def __init__(self):
        mongodb_name = settings['MONGODB_DBNAME']
        host = settings['MONGODB_HOST']
        port = settings['MONGODB_PORT']
        client = pymongo.MongoClient(host=host, port=port)
        db = client[mongodb_name]
        self.post = db[settings['MONGODB_DOCNAME']]

    def process_item(self, item, spider):
        book_info = dict(item)
        self.post.insert(book_info)
        return item

