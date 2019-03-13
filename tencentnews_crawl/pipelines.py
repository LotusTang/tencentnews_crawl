# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import urllib.request
import urllib.response
import os
import json
import logging


class TencentnewsCrawlPipeline(object):
    def process_item(self, item, spider):
        return item


class MoviePipeline(object):

    def open_spider(self, spider):
        self.file = open("my_meiju.txt", 'w', encoding='utf-8')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        self.file.write(item['name'] + "\n")
        return item


class XiaohuaPipeline(object):
    def process_item(self, item, spider):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0'}
        req = urllib.request.Request(url=item['addr'], headers=headers)
        res = urllib.request.urlopen(req)
        file_name = os.path.join(r'F:\PythonProject\xiaohuaPic', item['name']+'.jpg')
        with open(file_name, 'wb') as fp:
            fp.write(res.read())


class TestSplashPipeline(object):
    def open_spider(self, spider):
        self.file = open("jindongshouji.txt", 'w', encoding='utf-8')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        logging.debug("直接转换item:" + str(dict(item)))
        line = json.dumps(dict(item), ensure_ascii=False)
        self.file.write(line)
        return item


# 腾讯新闻链接测试
class TencentNewsUrlTest(object):
    def open_spider(self, spider):
        self.file = open("tencenturls.txt", 'w', encoding='utf-8')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        # logging.debug("直接转换item:" + str(dict(item)))
        line = str(dict(item)) + "\n"
        self.file.write(line)
        return item
