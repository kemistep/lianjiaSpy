这个爬虫主要验证了scrapy中 Rule的运行机制
=============================================================
 - 爬虫参考了知乎-李宏杰的爬虫项目：https://zhuanlan.zhihu.com/p/25278552</br>
--------------------------------------------------------------------
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
--------------------------------------------------------------------
首先对`start_urls`中的链接发起`request`,服务器会返回`response`。利用`Rule`中的规则提取链接，对提取到的链接发起`request`从而得到新的`response`，再调用`callback`的回调函数提取我们想得到的信息。

------------------------------------------------------------------
```
class OrangeSpider(CrawlSpider):
    name = 'orange'
    allowed_domains = ['anjuke.com']
    start_urls = ['https://tj.fang.anjuke.com/loupan/all/p1_w1/']
    rules = (
        Rule(LinkExtractor(
            allow=('https://tj.fang.anjuke.com/loupan/all/p\d+_w1/'),
            restrict_xpaths=("//div[@class='list-page']/div[1]/a[@class='next-page next-link']")
        )),
        Rule(LinkExtractor(
            allow=('https://tj.fang.anjuke.com/loupan/\d+.html'),
            restrict_xpaths=("//div[@class='list-contents']/div[1]/div[3]"),
            allow_domains='anjuke.com'), callback='parse_item', follow=False),
    ）
    
    def parse_item(self, response):
        item = AnjukeSpiderItem()
        item['house_name'] = response.xpath("//div[@class='lp-tit']/h1/text()").extract()
        item['house_price'] = response.xpath(
            "//div[@id='container']//dl[@class='basic-parms clearfix']/dd[@class='price']/p/em/text()").extract()
        item['house_location'] = response.xpath(
            "//div[@id='container']//span[@class='lpAddr-text']/text()").extract()
        item['house_open_and_sell_time'] = response.xpath(
            "//div[@id='container']/div[1]/div[2]/div[@class='brief-info basic-parms']/p/text()").extract()
        item['house_url'] = response.xpath("//head/link[1]/@href").extract()
        yield item
```
--------------------------------------------------------------------
* 还是先从`start_urls`中的链接得到返回的`response`，利用`Rule`提取链接，第一个提取到的是下一页的链接，第二个提取到的是每一个`item`的链接。</br>
* 先对得到的`item`链接发起请求，得到`response`，再调用回调函数`parse_item`提取感兴趣的信息。</br>
* 再对得到的下一页的链接发起请求，得到下一页的`response`，没有写回调函数，将再利用`Rule`提取链接，提取到第二页的`item`链接和第三页的链接并循环往复直到不能提取到链接。</br>
 - 此处参考的文章是：https://blog.csdn.net/wqh_jingsong/article/details/56865433
 -------------------------------------------------------------------
 v1.0中的是最新版本，可以实现翻页爬取
