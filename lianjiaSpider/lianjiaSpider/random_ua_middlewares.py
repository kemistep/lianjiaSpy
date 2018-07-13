import random
from scrapy.contrib.downloadermiddleware.useragent import UserAgentMiddleware
from lianjiaSpider.settings import UAPOOL


class RandomUserAgent(UserAgentMiddleware):
    def __init__(self, user_agent):
        self.user_agent = user_agent

    def process_request(self, request, spider):
        random_ua = random.choice(UAPOOL)
        print("当前使用的user-agent是：" + random_ua)
        request.headers.setdefault('User-Agent', random_ua)
