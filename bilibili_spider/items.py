# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class VideoItem(scrapy.Item):
    aid = scrapy.Field()  # 视频av号
    tid = scrapy.Field()  # 视频分区编号
    tname = scrapy.Field()  # 视频标签名称
    title = scrapy.Field()  # 视频标题

    date = scrapy.Field()  # 投稿日期
    time_ = scrapy.Field()  # 投稿时间
    now = scrapy.Field()  # 爬取时间

    desc = scrapy.Field()  # 视频描述
    dynamic = scrapy.Field()  # 视频标签，是一个list

    o_mid = scrapy.Field()  # 投稿up主id
    o_name = scrapy.Field()  # 投稿up主名称

    view = scrapy.Field()  # 观看数
    danmaku = scrapy.Field()  # 弹幕数
    reply = scrapy.Field()  # 评论数
    favorite = scrapy.Field()  # 收藏数
    coin = scrapy.Field()  # 硬币数
    share = scrapy.Field()  # 分享数
    like = scrapy.Field()  # 点赞数


class UserItem(scrapy.Item):
    mid = scrapy.Field()
    name = scrapy.Field()
    sex = scrapy.Field()
    sign = scrapy.Field()
    level = scrapy.Field()
    desc = scrapy.Field()
    viptype = scrapy.Field()

    following = scrapy.Field()
    follower = scrapy.Field()
    v_view = scrapy.Field()
    a_view = scrapy.Field()
    likes = scrapy.Field()

    video = scrapy.Field()
    article = scrapy.Field()
    album = scrapy.Field()
    audio = scrapy.Field()
