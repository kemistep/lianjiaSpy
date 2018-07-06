# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy import Request
from scrapy.loader.processors import Join
from scrapy.loader import ItemLoader
from lianjiaSpider.items import LianjiaspiderItem


class LianjiaSpider(CrawlSpider):
    name = 'lianjia'
    allowed_domains = ['lianjia.com']
    start_urls = ['https://bj.lianjia.com/zufang/pg1/']

    rules = (
        Rule(LinkExtractor(
            restrict_xpaths='//div[@class="bd"]/dl[1]/dd/div/a[1]'),
            callback='next_page'),
    )

    def next_page(self, response):
        page_url = response.xpath('//@page-url').extract_first()
        page_data = response.xpath("//@page-data").extract_first()
        if page_url == None:
            pass
        else:
            total_page = eval(page_data)['totalPage']
            for page in range(1, total_page):
                rel_url = page_url.format(page=page)
                yield Request(url=response.urljoin(rel_url), callback=self.parse_item)

        '''
        page_data : /zufang/pg{page}l1/
        total_page : 86
        rel_url : /zufang/pg1l1/
        url : 'https://bj.lianjia.com/zufang/pg1l1/'
        '''

    def parse_item(self, response):
        l = ItemLoader(item=LianjiaspiderItem(), response=response, )
        l.default_output_processor = Join()
        l.add_xpath('url', '//ul[@id="house-lst"]/li/div[2]/div[2]/div[1]/span/text()')
        item = l.load_item()
        yield item
