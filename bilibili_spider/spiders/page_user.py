# -*- coding: utf-8 -*-
import scrapy
import json
import re
from scrapy.http import Request
import time
import requests

from bilibili_spider.items import UserItem

'''
从我的空间进入
爬取基本信息，将数据带入下一层函数
爬取成就信息，按上步的方法一直爬取然后丢进pipeline
进入follower和following，（爬取基本信息）在for循环中深度优先遍历

还是按第一版，同一在navnum里yield item

'''


class PageUserSpider(scrapy.Spider):
    name = 'page_user'
    allowed_domains = ['api.bilibili.com']
    mid = 43
    start_urls = ['https://api.bilibili.com/x/space/acc/info?mid='+str(mid)]
    custom_settings = {
        'ITEM_PIPELINES': {'bilibili_spider.pipelines.UserPipeline': 300},
    }
    from fake_useragent import UserAgent
    ua = UserAgent()
    headers = {
        'User-Agent': ua.chrome
    }

    def parse(self, response):
        res = json.loads(response.body)
        if not res['code']:
            data = res['data']
            stat_url = 'https://api.bilibili.com/x/relation/stat?vmid=' + str(data['mid'])
            stat = json.loads(requests.get(stat_url, headers=self.headers).text)

            params = dict(
                mid=data['mid'],
                name=data['name'],
                sex=data['sex'],
                sign=data['sign'],
                level=data['level'],
                desc=data['official']['title'],
                viptype=data['vip']['type'],
                following=stat['data']['following'],
                follower=stat['data']['follower'],

            )
            navnum_url = 'https://api.bilibili.com/x/space/navnum?mid=' + str(data['mid'])
            yield Request(navnum_url, meta=params, callback=self.parse_navnum)

        self.mid += 1
        next_url = 'https://api.bilibili.com/x/space/acc/info?mid=' + str(self.mid)
        self.headers['User-Agent'] = self.ua.chrome
        yield Request(next_url, callback=self.parse)


        # # 获得所有follow的mid
        # mid_lis = [user['mid'] for user in res['data']['list']]
        # for m in mid_lis:
        #     info_url = 'https://api.bilibili.com/x/space/acc/info?mid=' + str(m) + '&ps=6'
        #     yield Request(info_url, callback=self.parse_info)
        #
        #     fing_url = 'https://api.bilibili.com/x/relation/followings?vmid=' + str(m) + '&ps=6'
        #     yield Request(fing_url, callback=self.parse)
        #
        #     # fer_url = 'https://api.bilibili.com/x/relation/followers?vmid=' + str(m) + '&ps=6'
        #     # yield Request(fer_url, callback=self.parse)

    # def parse_info(self, response):
    #     res = json.loads(response.body)
    #     data = res['data']
    #     stat_url = 'https://api.bilibili.com/x/relation/stat?vmid=' + str(data['mid'])
    #     stat = json.loads(requests.get(stat_url, headers=self.headers).text)
    #
    #     params = dict(
    #         mid=data['mid'],
    #         name=data['name'],
    #         sex=data['sex'],
    #         sign=data['sign'],
    #         level=data['level'],
    #         desc=data['official']['title'],
    #         viptype=data['vip']['type'],
    #         following=stat['data']['following'],
    #         follower=stat['data']['follower'],
    #
    #     )
    #     navnum_url = 'https://api.bilibili.com/x/space/navnum?mid=' + str(data['mid'])
    #     yield Request(navnum_url, meta=params, callback=self.parse_navnum)

    # def parse_achive(self, response):
    #     res = json.loads(response.body)
    #     data = res['data']
    #     params = response.meta
    #
    #     params['following'] = data['following']
    #     params['follower'] = data['follower']
    #
    #     upstat_url = 'https://api.bilibili.com/x/space/upstat?mid=' + str(params['mid'])
    #     yield Request(upstat_url, meta=params, callback=self.parse_upstat)

    # def parse_upstat(self, response):
    #     res = json.loads(response.body)
    #     data = res['data']
    #     params = response.meta
    #
    #     params['v_view'] = data['archive']['view']
    #     params['a_view'] = data['article']['view']
    #     params['likes'] = data['likes']
    #
    #     navnum_url = 'https://api.bilibili.com/x/space/navnum?mid=' + str(params['mid'])
    #     yield Request(navnum_url, meta=params, callback=self.parse_navnum)

    def parse_navnum(self, response):
        res = json.loads(response.body)
        data = res['data']
        params = response.meta
        upstat_url = 'https://api.bilibili.com/x/space/upstat?mid=' + str(params['mid'])
        upstat = json.loads(requests.get(upstat_url, headers=self.headers).text)

        item = UserItem()
        item['mid'] = params['mid']
        item['name'] = params['name']
        item['sex'] = params['sex']
        item['sign'] = params['sign']
        item['level'] = params['level']
        item['desc'] = params['desc']
        item['viptype'] = params['viptype']

        item['following'] = params['following']
        item['follower'] = params['follower']
        item['v_view'] = upstat['data']['archive']['view']
        item['a_view'] = upstat['data']['article']['view']
        item['likes'] = upstat['data']['likes']

        item['video'] = data['video']
        item['article'] = data['article']
        item['album'] = data['album']
        item['audio'] = data['audio']

        yield item
