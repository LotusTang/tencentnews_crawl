import scrapy
import logging
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from scrapy.selector import Selector
from scrapy_splash import SplashRequest
from tencentnews_crawl.items import TencentNewsUrl


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
        "https://news.qq.com/",
    ]


    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse,  args={'wait': 10}, )

    # 只抓取一个页面作为示例，
    def parse(self, response):
        site = Selector(response)
        # =_=,我写了这么多，好像就只有 //ul[@class="list"]/li 捞取基本所有url???
        # 定义使用到的set变量
        it__huati_urls = set()
        it_jiaozhen_urls = set()
        guyu_urls = set()

        # 抓取今日要闻URL
        # today_yaowenurls = site.xpath('//ul[@class="list top-list"]/li')
        # for today_yaowenurl in today_yaowenurls:
        #     it = TencentNewsUrl()
        #     it['url'] = today_yaowenurl.xpath('./div/h3/a/@href').extract()
        #     yield it
        # 不需要像上面那么繁琐，直接使用就好，而且使用上面的方式，每次调用xpath返回的都是一个SelectorList对象
        # 然后结果extract()调用都会返回一个列表，其实我们不需要列表，只需要一个字符串对象就行
        today_yaowenurls = site.xpath('//ul[@class="list top-list"]/li/div/h3/a/@href')
        for today_yaowenurl in today_yaowenurls:
            yield TencentNewsUrl(url=today_yaowenurl.extract())
        # 抓取今日话题URL 以及 谷雨URL
        today_yaowen_guyu_urlurls = site.xpath('//div[@class="news-bar news-huati"]/div[2]/ul/li//a/@href')
        for today_huati_guyu_item in today_yaowen_guyu_urlurls:
            if today_huati_guyu_item.extract() not in it__huati_urls:
                it__huati_urls.add(today_huati_guyu_item.extract())
                yield TencentNewsUrl(url=today_huati_guyu_item)
        # 较真URL
        jiaozhenlist = site.xpath('//div[@class="news-bar news-jiaozhen"]/div[2]/ul/li')
        for jiaozhenurlitem in jiaozhenlist:
            it_jiaozhen_urls.add(jiaozhenurlitem.xpath('.//a/@href').extract())
        for it_jiaozhen_url in it__huati_urls:
            yield TencentNewsUrl(url=it_jiaozhen_url)
        # 谷雨URL
        # guyu_urllist = site.xpath('//div[@class="news-bar news-huati"][2]/div[2]/ul')
        # for guyu_url_item in guyu_urllist:
        #     guyu_urls.add(guyu_url_item.xpath('.//a/@href').extract())
        # for guyu_url in guyu_urls:
        #     yield TencentNewsUrl(url=guyu_url)
        # 热门资讯
        remenzixun_urllist = site.xpath('//div[@class="hot-bar"]/div[2]/ul/li/div[2]/a/@href')
        for remenzixun_urlitem in remenzixun_urllist:
            yield TencentNewsUrl(url=remenzixun_urlitem.extract())
        # 热点精选
        redianjinxuan_urllist = site.xpath('//div[@class="channel_mod"]/ul[2]/li/a/@href')
        for redianjinxuan_urlitem in redianjinxuan_urllist:
            yield TencentNewsUrl(url=redianjinxuan_urlitem.extract())
        # 直接打印所有的response
        file_response = open("tencent_response.txt", 'w', encoding='utf-8')
        file_response.write(str(response.xpath('/html').extract()))
        # 测试另外的xpath
        logging.debug("sidebar xpath 测试: " + str(site.xpath('//div[@class="sidebar fr"]/div/div').extract()))
        logging.debug("mainbar xpath 测试: " + str(site.xpath('//div[@class="main fl"]').extract()))
        logging.debug("较真 xpath 测试: " + str(site.xpath('//div[@class ="news-bar news-jiaozhen"]/div[2]/ul/li').extract()))



