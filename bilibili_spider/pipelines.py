# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import MySQLdb
import MySQLdb.cursors

from twisted.enterprise import adbapi


class VideoPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        # 键要和MySQLdb中的参数对应
        db_args = dict(
            host=settings['MYSQL_HOST'],
            database=settings['MYSQL_DATABASE'],
            port=settings['MYSQL_PORT'],
            user=settings['MYSQL_USER'],
            password=settings['MYSQL_PSWD'],
            charset='utf8',
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=True
        )
        dbpool = adbapi.ConnectionPool('MySQLdb', **db_args)
        # 相当于dbpool付给了这个类
        return cls(dbpool)

    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self.sql_insert, item)
        query.addErrback(self.handle_error)
        return item

    @staticmethod
    def sql_insert(cursor, item):
        # 需要where not exist
        state = """
                       insert ignore into video(aid, tid, tname, title, date, time, now, descs, dynamic, o_mid, o_name, views, danmakus, replies, favorites, coins, shares, likes)
                       values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
           """
        # twisted会自动commit
        cursor.execute(state, (item['aid'], item['tid'], item['tname'], item['title'], item['date'],
                               item['time_'], item['now'], item['desc'], item['dynamic'], item['o_mid'],
                               item['o_name'], item['view'], item['danmaku'], item['reply'], item['favorite'],
                               item['coin'], item['share'], item['like']))
        # 更新操作要另外写
        return item

    @staticmethod
    def handle_error(failure, item, spider):
        print(failure)


class UserPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        # 键要和MySQLdb中的参数对应
        db_args = dict(
            host=settings['MYSQL_HOST'],
            database=settings['MYSQL_DATABASE'],
            port=settings['MYSQL_PORT'],
            user=settings['MYSQL_USER'],
            password=settings['MYSQL_PSWD'],
            charset='utf8',
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=True
        )
        dbpool = adbapi.ConnectionPool('MySQLdb', **db_args)
        # 相当于dbpool付给了这个类
        return cls(dbpool)

    def process_item(self, item, spider):
        if item['type'] == 'basic':
            query = self.dbpool.runInteraction(self.sql_insert, item)  # 写两个函数或添加一个参数
        elif item['type'] == 'achieve':
            query = self.dbpool.runInteraction(self.sql_insert, item)
        query.addErrback(self.handle_error)
        return item

    @staticmethod
    def sql_insert(cursor, item):
        # 需要where not exist
        state = """
                       insert ignore into video(aid, tid, tname, title, date, time, now, descs, dynamic, o_mid, o_name, views, danmakus, replies, favorites, coins, shares, likes)
                       values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
           """
        # twisted会自动commit
        cursor.execute(state, (item['aid'], item['tid'], item['tname'], item['title'], item['date'],
                               item['time_'], item['now'], item['desc'], item['dynamic'], item['o_mid'],
                               item['o_name'], item['view'], item['danmaku'], item['reply'], item['favorite'],
                               item['coin'], item['share'], item['like']))
        # 更新操作要另外写
        return item

    @staticmethod
    def handle_error(failure, item, spider):
        print(failure)
