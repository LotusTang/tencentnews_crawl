import scrapy
import logging
from tencentnews_crawl.items import MovieItem


class MeijuSpider(scrapy.Spider):
    name = "meiju"
    allowed_domains = ['meijutt.com']
    start_urls = ['http://www.meijutt.com/new100.html']

    # 默认使用parse做为解析response,但是如果是其它Spider，比如
    # crawlspider可能会不同
    def parse(self, response):
        logging.debug("这是抓取美剧天堂的数据")
        movies = response.xpath('//ul[@class="top-list  fn-clear"]/li')
        logging.debug("response li:" + movies)
        for each_movie in movies:
            item = MovieItem()
            logging.debug("each_movie xpath:" + each_movie.xpath('./h5/a/@title'))
            item['name'] = each_movie.xpath('./h5/a/@title').extract()[0]
            yield item





