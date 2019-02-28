import scrapy
from tencentnews_crawl.items import XiaohuaItem


# 我们可以将其修改为进阶篇，就是获取所有链接然后进行抓取
class XiaohuaSpider(scrapy.Spider):
    name = "xiaohua"
    allowed_domain = ["xiaohuar.com"]
    start_urls = ['http://www.xiaohuar.com/list-1-1.html']
    url_set = set()

    def parse(self, response):
        if response.url.startswith('http://www.xiaohuar.com/list-'):
            allPics = response.xpath('//div[@class="img"]/a')
            for pic in allPics:
                item = XiaohuaItem()
                item['name'] = pic.xpath("./img/@alt").extract()[0]
                item['addr'] = 'http://www.xiaohuar.com' + pic.xpath("./img/@src").extract()[0]
                yield item
        # 获取所有链接，并将所有满足条件的链接都放到一个set对象里去
        # 这样做的话，就是使用set,很简单粗暴的将所有不重复的链接都爬取直到没有重复的链接为止
        urls = response.xpath("//a/@href").extract()
        for url in urls:
            if url.startswith('http://www.xiaohuar.com/list-'):
                if url in self.url_set:
                    pass
                else:
                    self.url_set.add(url)
                    yield self.make_requests_from_url(url)
                    # make_requests_from_url就是返回了一个Request对象这样
                    # Request(url, dont_filter=True)
                    # 当然我们可以自己直接yield不需要调用这个方法
            else:
                pass
        # 这样就顺利将所有的该抓取的都抓完了，但是觉得就是太简单粗暴了，没有精细化的感觉











