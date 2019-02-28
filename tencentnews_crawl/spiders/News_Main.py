import scrapy
import logging
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from scrapy.selector import Selector


# 爬取腾讯新闻首页的例子
class NewsMainSpider(scrapy.spiders.CrawlSpider):
    # 我们调用命令启动爬虫的时候需要这个名字
    name = "newsqq"
    allowed_domains = [
        "news.qq.com",
        "new.qq.com",
        "i.match.qq.com"
    ]
    start_urls = [
        "https://i.match.qq.com/ninja/fragcontent?pull_urls=news_top_2018&callback=__jp1",
    ]

    # 分别写出四种链接形式的正则表达式
    url_pattern1 = r'http(.*)/omn/([A-Z0-9]{16,19})'
    url_pattern2 = r'http(.*)/omn/(\d{8})/(.+)\.html'
    url_pattern3 = r'http(.*)/cmsn/([A-Z0-9]{16,19})'
    url_pattern4 = r'http(.*)/cmsn/(\d{8})/(.+)\.html'
    url_pattern5 = r'http(.*)/a/(\d{8})/(\d+)\.htm'
    url_pattern2_test = r'http(.*)/omn\\\\/(\d{8})\\\\/(.+)\.html'

    # 由于crawlSpider的特点，所以我们选择使用规则去提取对应的链接
    rules = (
        Rule(LinkExtractor(allow=(url_pattern1,)), 'parse_news1'),
        Rule(LinkExtractor(allow=(url_pattern2,)), 'parse_news2'),
        Rule(LinkExtractor(allow=(url_pattern3,)), 'parse_news3'),
        Rule(LinkExtractor(allow=(url_pattern4,)), 'parse_news4'),
        Rule(LinkExtractor(allow=(url_pattern2_test,)), 'parse_news2')
    )

    def parse_news1(self, response):
        logging.debug("This is a debug from parse_news1")
        sel = Selector(response)
        print(response.url)

    def parse_news2(self, response):
        logging.debug("This is a warning from parse_news2")
        sel = Selector(response)
        print(response.url)

    def parse_news3(self, response):
        logging.debug("This is a warning from parse_news3")
        sel = Selector(response)
        print(response.url)

    def parse_news4(self, response):
        logging.debug("This is a warning from parse_news4")
        sel = Selector(response)
        print(response.url)

