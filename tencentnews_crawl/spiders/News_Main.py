import scrapy
import logging


# 爬取腾讯新闻首页的例子
class NewsMainSpider(scrapy.Spider):

    name = "news_main_spider"

    allowed_domains = [
        "news.qq.com"
    ]

    start_urls = [
        "https://news.qq.com/"
    ]

    def parse(self, response):
        logging.warning("This is a warning")



