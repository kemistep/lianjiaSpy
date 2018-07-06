本爬虫爬取的是链家的北京二手房信息，主要验证了scrapy rules的运行机制
===
 - 爬虫入口网址：https://bj.lianjia.com/zufang/</br>
 - 参考了知乎-李宏杰的爬虫项目：https://zhuanlan.zhihu.com/p/25278552</br>
---------------
```
class LianjiaSpider(CrawlSpider):
    name = 'lianjia'
    allowed_domains = ['lianjia.com']
    start_urls = ['https://bj.lianjia.com/zufang/pg1l1/']
    rules = (
        Rule(LinkExtractor(restrict_xpaths='//ul[@id="house-lst"]/li/div[2]/h2/a'), callback='parse_item'),
    )

    def parse_item(self, response):
        l = ItemLoader(item=LianjiaspiderItem(), response=response, )
        l.default_output_processor = Join()
        l.add_xpath('url', '//div[@class="content zf-content"]/div[1]/span[1]/text()')
        item = l.load_item()
        yield item
```
首先对`start_urls`中的链接发起`request`,服务器会返回`response`
