# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from ele_poiid.pymysqlpool import ConnectionPool
from ele_poiid import  settings


class ElePoiidPipeline(object):
    def __init__(self):
        config = dict(
            pool_name='eleshop',
            host=settings.MYSQL_HOST,  # 读取settings中的配置
            port=settings.MYSQL_PORT,
            user=settings.MYSQL_USER,
            password=settings.MYSQL_PASSWD,
            database=settings.MYSQL_DBNAME,
            charset='utf8',  # 编码要加上，否则可能出现中文乱码问题
        )
        self.pool = ConnectionPool(**config)

    def process_item(self, item, spider):
        with self.pool.cursor() as cursor:
            cursor.execute(
                "INSERT INTO ele_id (poi_id, name, address) VALUES (%s, %s, %s)",
                (item["poi_id"], item["name"], item["address"]))

    def close_spider(self,spider):
        self.pool.close()

