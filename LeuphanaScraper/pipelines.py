# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import os
import re
import json
import logging
import psycopg2
import psycopg2.extras
import scrapy
from psycopg2.errors import UniqueViolation
from LeuphanaScraper.definitions import CONFIG_DIR
from scrapy.pipelines.images import ImagesPipeline


class LeuphanascraperPipeline:
    def process_item(self, item, spider):
        return item


class NewsPipeline(object):
    def __init__(self):
        super().__init__()
        self.logger = logging.Logger(self.__class__.__name__)
        with open(os.path.join(CONFIG_DIR, 'postgres.json'), 'r', encoding='utf-8') as f:
            config = json.load(f)
        self.conn = psycopg2.connect(
            dbname=config['dbname'],
            user=config['user'],
            password=config['password'],
            host=config['host'],
            port=config['port']
        )
        # transaction isolation level, autocommit means no transaction
        # self.conn.isolation_level = psycopg2.extensions.ISOLATION_LEVEL_READ_UNCOMMITTED
        self.conn.autocommit = True
        psycopg2.extensions.register_adapter(dict, psycopg2.extras.Json)
        self.cur = self.conn.cursor()
        # used to extract numbers
        self.regex = re.compile(r"\d+\d*")

    def open_spider(self, spider):
        if spider.name != "news":
            del self.conn
            del self.cur

    def process_item(self, item, spider):
        if spider.name == "news":
            # since major of fileds are char type, set each to empty string
            for k, v in item.items():
                item[k] = '' if not item[k] else item[k]

            item["pub_year"] = int(item["pub_year"])
            item["pub_month"] = int(item["pub_month"])
            item["pub_day"] = int(item["pub_day"])

            table_name = 'news'
            sql = 'INSERT INTO %s (%s) VALUES (%%(%s)s );' % (table_name, ', '.join(item), ')s, %('.join(item))
            try:
                self.cur.execute(sql, dict(item))
                self.conn.commit()
            except UniqueViolation as e:
                pass

        return item

    def close_spider(self, spider):
        if spider.name == "news":
            self.cur.close()
            self.conn.close()