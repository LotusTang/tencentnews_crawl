# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Item
from scrapy import Field


# 腾讯新闻模板
class TencentnewsCrawlItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


# 设置一个电影模板，从美剧天堂获取数据
class MovieItem(Item):
    name = scrapy.Field()


# 校花网获取数据模板
class XiaohuaItem(Item):
    addr = scrapy.Field()
    name = scrapy.Field()


# 测试Splash抓取京东商品使用的优惠券
class SplashTestItem(Item):
    price = Field()
    promotion = Field()
    value_add = Field()
    quality = Field()
    color = Field()
    version = Field()
    suit = Field()
    value_add_protection = Field()
    staging = Field()



