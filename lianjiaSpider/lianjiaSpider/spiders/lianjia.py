# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy import Request
from scrapy.loader.processors import Join
from scrapy.loader import ItemLoader
from lianjiaSpider.items import LianjiaspiderItem
import re


class LianjiaSpider(CrawlSpider):
    name = 'lianjia'
    allowed_domains = ['lianjia.com']
    start_urls = ['https://bj.lianjia.com/zufang/pg1/']

    rules = (
        Rule(LinkExtractor(
            # allow='/\w+/\w+/',
            restrict_xpaths='//div[@class="bd"]/dl[1]/dd/div/a[1]'),
            callback='next_page'),
        # Rule(LinkExtractor(restrict_xpaths='//div[@class="bd"]/dl[1]/dd/div/a[1]'), callback='next_page'),
        # Rule(LinkExtractor(restrict_xpaths='//ul[@id="house-lst"]/li/div[2]/h2/a'), callback='parse_item',
        #      follow=False),
    )

    # allow = ('https://bj.lianjia.com/zufang/\d+.html'),
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
        page_data : /zufang/pg{page}/
        total_page : 86
        rel_url : /zufang/pg1/
        url : 'https://bj.lianjia.com/zufang/pg1/'
        '''

    def parse_item(self, response):
        # for list in response.xpath("//ul[@id='house-lst']/li"):
        l = ItemLoader(item=LianjiaspiderItem(), response=response, )
        l.default_output_processor = Join()
        l.add_xpath('house_price', '//ul[@id="house-lst"]/li/div[2]/div[2]/div[1]/span/text()')
        l.add_xpath('house_url', '//ul[@id="house-lst"]/li/div[2]/h2/a/@href')
        l.add_xpath('title', '//ul[@id="house-lst"]/li/div[2]/h2/a/@title')
        l.add_xpath('house_zone', '//ul[@id="house-lst"]/li/div[2]/div[1]/div[1]/span[1]/span/text()', re=r'\d室\d厅')
        l.add_xpath('house_location', '//ul[@id="house-lst"]/li/div[2]/div[1]/div[@class="other"]/div/a/text()',
                    re=r'\w+[^(租房)]')
        l.add_xpath('community', '//ul[@id="house-lst"]/li/div[2]/div[1]/div[@class="where"]/a/span/text()',
                    re=r'\w+[^(\xa0)]')
        l.add_xpath('house_area', '//ul[@id="house-lst"]/li/div[2]/div[1]/div[@class="where"]/span[2]/text()',
                    re=r'\w+[^(\xa0)]')
        item = l.load_item()
        yield item
