# -*- coding: utf-8 -*-
import pymysql
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


#class BhunewSpiderPipeline(object):
#    def process_item(self, item, spider):
#        return item
#mysql数据库
class MysqlPipeline(object):
    def process_item(self, item, spider):
        conn = pymysql.connect(
            host='localhost',
            user='root',
            passwd='root',
            charset='utf8'
        )
        cursor = conn.cursor()
        conn.select_db('bhu_news')

        #list转为str, 提交数据
        title = "".join(item['title'])
        time = "".join(item['time'])
        people = "".join(item['people'])
        content = "".join(item['content'])

        sql = "insert into bhu_news(title,people,time,content) values(%s,%s,%s,%s)"
        data = (title, people, time, content)
        cursor.execute(sql, data)
        conn.commit()

        cursor.close()
        conn.close()

        return item
'''
CREATE DATABASE bhu_news DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;

CREATE TABLE `bhu_news` (
  `title` text COMMENT '标题',
  `content` text COMMENT '文章内容',
  `people` text  COMMENT '供稿人',
  `time` text  COMMENT '文章发布时间'
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

'''