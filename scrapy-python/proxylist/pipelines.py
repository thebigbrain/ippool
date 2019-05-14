# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import hashlib

from elasticsearch import Elasticsearch

from leveldb.db import LevelDB


class ElasticSearchPipeline(object):
    def __init__(self, host, port):
        self.es_host = host
        self.es_port = port

        self.es = None

    @classmethod
    def from_crawler(cls, crawler):
        return cls(host=crawler.settings.ES_HOST, port=crawler.settings.ES_PORT)

    def open_spider(self, spider):
        self.es = Elasticsearch([{'host': self.es_host, 'port': self.es_port}])

    def close_spider(self, spider):
        pass

    def process_item(self, item, spider):
        doc_id = item['ip'] + ':' + item['port']
        self.es.index(index='ippool', doc_type=item['protocol'], id=doc_id, body=item)
        return item


class LevelDBPipeline(object):
    def __init__(self, filename):
        self.filename = filename
        self.db = None

    @classmethod
    def from_crawler(cls, crawler):
        return cls(filename=crawler.settings.get('LEVELDB_FILENAME'))

    def open_spider(self, spider):
        self.db = LevelDB.open(self.filename)

    def close_spider(self, spider):
        self.db.close()

    def process_item(self, item, spider):
        key = LevelDBPipeline.md5(item)
        self.db.put(key, item)
        return item

    @staticmethod
    def md5(item):
        return hashlib.md5(
            ':'.join([item.get('protocol'), item.get('ip'), item.get('port')]).encode('utf-8')
        ).digest()
