# -*- coding: utf-8 -*-
import scrapy
import json
import re
from scrapy.http import Request
import time

from bilibili_spider.items import VideoItem

'''
每次爬取pn+1，直到['data']['page']['count']==0
'''


class PageVideoSpider(scrapy.Spider):
    name = 'page_video'
    # 一定要是域名！！
    allowed_domains = ['api.bilibili.com']
    # 0和1是同一页,173=60*60*24/10/50
    pn = 174
    start_urls = ['https://api.bilibili.com/x/web-interface/newlist?rid=24&pn='+str(pn)]
    custom_settings = {
        'ITEM_PIPELINES': {'bilibili_spider.pipelines.VideoPipeline': 300},
    }

    # 采用广度优先
    rids = [
        24, 25, 47, 86, 27,  # 动画
        # 33, 32, 51, 152,  # 番剧
        168,  # 153, 169, 195, 170,  # 国创
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
        # 37, 178, 179, 180,  # 纪录片
        # 147, 145, 146, 83,  # 电影
        # 185, 187  # 电视剧
    ]
    # 从第二个开始
    point = 1
    # headers = {
    #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
    #                   'Chrome/80.0.3987.132 Safari/537.36 '
    # }

    def parse(self, response):
        res = json.loads(response.body)

        if res['data']['page']['count'] == 0:
            del self.rids[self.point]
        if not self.rids:
            self.crawler.engine.close_spider(self, '所有分区爬取完毕，爬虫停止')

        for video in res['data']['archives']:

            try:
                aid = video['aid']  # av号
                tid = video['tid']  # 分区号
                tname = video['tname']  # 最下级分区
                title = video['title']

                stime = time.localtime(video['pubdate'])  # 投稿时间戳，需分离
                date = time.strftime('%Y-%m-%d', stime)
                time_ = time.strftime('%H:%M:%S', stime)
                now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

                desc = video['desc']  # 视频介绍
                dynamic = video['dynamic']  # 标签
                if dynamic:
                    dynamic = str(re.findall(r'(?<=#)[^#\s]+?(?=#)', dynamic))

                o_mid = video['owner']['mid']
                o_name = video['owner']['name']

                stat = video['stat']
                view = stat['view']
                danmaku = stat['danmaku']  # 弹幕数
                reply = stat['reply']
                favorite = stat['favorite']  # 收藏数
                coin = stat['coin']
                share = stat['share']
                like = stat['like']  # 点赞数

                #  存储进item
                item = VideoItem()
                item['aid'] = aid
                item['tid'] = tid
                item['tname'] = tname
                item['title'] = title
                item['date'] = date
                item['time_'] = time_
                item['now'] = now
                item['desc'] = desc
                item['dynamic'] = dynamic
                item['o_mid'] = o_mid
                item['o_name'] = o_name
                item['view'] = view
                item['danmaku'] = danmaku
                item['reply'] = reply
                item['favorite'] = favorite
                item['coin'] = coin
                item['share'] = share
                item['like'] = like
                yield item
                # time.sleep(0.1)

            except KeyError:
                print('{0:-^50}'.format('[waring]keyError'))
                print('{0:-^50}'.format('[tid]' + video['tid']))
                print('{0:-^50}'.format('[aid]' + video['aid']))
                now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                with open('ErrorLog.txt', 'a') as f:
                    f.write(video['tid'] + '   ' + video['aid'] + '   ' + now + '\n')
                raise KeyError
                # continue

        self.point = (self.point + 1) % len(self.rids)
        if self.point == 0:
            self.pn += 1
            next_url = re.sub(r'(?<=pn=)\d+', str(self.pn), response.url)  # 多余了
            next_url = re.sub(r'(?<=rid=)\d+', str(self.rids[self.point]), next_url)

        else:
            next_url = re.sub(r'(?<=rid=)\d+', str(self.rids[self.point]), response.url)
        yield Request(url=next_url, callback=self.parse)


'''
在rids中循环，
整个列表循环一遍后pn+1
当res['data']['page']['count']==0
则将当前rid从列表中移除
当列表为空后停止
'''
