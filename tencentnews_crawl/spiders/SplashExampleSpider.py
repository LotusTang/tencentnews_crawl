import scrapy_splash
import scrapy
from scrapy_splash import SplashRequest
from scrapy.selector import Selector
from tencentnews_crawl.items import SplashTestItem


class SplashExampleSpider(scrapy.Spider):
    name = "test_splash"
    start_urls = [
        'https://item.jd.com/100001550349.html'
    ]
    allowed_domain = [
        'item.jd.com'
    ]

    # 需要将Request封装成SplashRequest
    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse, args={'wait': 0.5})

    # 只抓取一个京东页面作为示例
    def parse(self, response):
        site = Selector(response)
        # it_list = []
        it = SplashTestItem()
        # 从站点中提取对应的Field
        prices = site.xpath('//span[@class="p-price"]/span/text()')
        it['price'] = prices[0].extract() + prices[1].extract()
        promotions = site.xpath(
            '//div[@class="prom-gift-list"]/div[@class="prom-gift-item"]/a/img/@src')
        it['promotion'] = ''
        for promotion in promotions:
            it['promotion'] += promotion.extract()
        it['value_add'] = site.xpath('//ul[@class="choose-support lh"]/li/a/span/text()').extract()
        it['quality'] = site.xpath('//div[@id="summary-weight"]/div[2]/text()').extract()
        colors = site.xpath('//div[@id="choose-attr-1"]/div[2]/div/@title')
        it['color'] = ''
        for color in colors:
            it['color'] += color.extract() + ' '
        versions = site.xpath('//div[@id="choose-attr-2"]/div[2]/div/@data-value')
        it['version'] = ''
        for version in versions:
            it['version'] += version.extract() + ' '
        it['suit'] = ''
        suits = site.xpath('//div[@id="choose-suits"]/div[2]/div/a/text()')
        for suit in suits:
            it['suit'] += suit.extract() + ' '
        it['value_add_protection'] = ''
        value_add_protections = site.xpath('//div[@class="yb-item-cat"]/div[1]/span[1]/text()')
        for value_add_protection in value_add_protections:
            it['value_add_protection'] += value_add_protection.extract()
        it['staging'] = ''
        stagings = site.xpath('//div[@class="baitiao-list J-baitiao-list"]/div[@class="item"]/a/strong/text()')
        for staging in stagings:
            it['staging'] += staging.extract()
        # it_list.append(it)
        return it










