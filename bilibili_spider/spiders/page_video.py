# -*- coding: utf-8 -*-
import scrapy
import json
import re
from scrapy.http import Request
import time
from urllib import parse

'''
每次爬取pn+1，直到['data']['page']['count']==0
'''


class PageVideoSpider(scrapy.Spider):
    name = 'page_video'
    # 一定要是域名！！
    allowed_domains = ['api.bilibili.com']
    start_urls = ['https://api.bilibili.com/x/web-interface/newlist?rid=24&pn=0']
    pn = 0
    # 采用广度优先
    rids = [24, 25, 47, 86, 27,  # 动画
            33, 32, 51, 152,  # 番剧
            153, 168, 169, 195, 170,  # 国创
            28, 31, 30, 194, 59, 193, 29, 130,  # 音乐
            20, 198, 199, 200, 154, 156,  # 舞蹈
            17, 171, 172, 65, 173, 121, 136, 19,  # 游戏
            124, 122, 39, 96, 98, 176,  # 科技
            95, 189, 190, 191,  # 数码
            138, 21, 76, 75, 161, 162, 163, 174,  # 生活
            22, 26, 126, 127,  # 鬼畜
            157, 158, 164, 159, 192,  # 生活
            166,  # 广告
            71, 137, 131,  # 娱乐
            182, 183, 85, 184,  # 影视
            37, 178, 179, 180,  # 纪录片
            147, 145, 146, 83,  # 电影
            185, 187  # 生活
            ]
    # 从第二个开始
    point = 1
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/80.0.3987.132 Safari/537.36 '
    }

    def parse(self, response):
        res = json.loads(response.body)

        for video in res['data']['archives']:
            try:
                aid = video['aid']  # av号
                tid = video['tid']  # 分区号
                tname = video['tname']  # 最下级分区
                title = video['title']
                stime = time.localtime(video['pubdate'])  # 投稿时间戳，需分离
                date = time.strftime('%Y-%m-%d', stime)
                when = time.strftime('%H:%M:%S', stime)
                now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

                desc = video['desc']  # 视频介绍
                dynamic = video['dynamic']  # 标签

                o_mid = video['owner']['mid']
                o_name = video['owner']['name']

                stat = video['stat']
                view = stat['view']
                danmaku = stat['danmaku']  # 弹幕数
                reply = stat['reply']
                favorite = stat['favorite']
                coin = stat['coin']
                share = stat['share']
                reply = stat['reply']
                like = stat['like']

                #  存储进item

            except KeyError:

                print('{0:-^50}'.format('[waring]keyError'))
                print('{0:-^50}'.format('[tid]' + video['tid']))
                print('{0:-^50}'.format('[aid]' + video['aid']))
                now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                with open('ErrorLog.txt', 'a') as f:
                    f.write(video['tid'] + '   ' + video['aid'] + '   ' + now + '\n')
                raise KeyError
                # continue

        # if res['data']['page']['count'] != 0:
        if self.point < len(self.rids):

            next_url = re.sub(r'(?<=rid=)\d+', str(self.rids[self.point]), response.url)
            # self.pn += 1
            # next_url = re.search(r'.+pn=', response.url).group(0) + str(self.pn)
            yield Request(url=parse.urljoin(response.url, next_url), callback=self.parse)
            print(self.rids[self.point], self.pn)

            self.point += 1
        else:
            # 退出语句
            pass
'''
在rids中循环，
整个列表循环一遍后pn+1
当res['data']['page']['count']==0
则将当前rid从列表中移除
当列表为空后停止
'''