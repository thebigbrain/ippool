# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from elasticsearch import Elasticsearch


class ElasticSearchPipeline(object):
    def __init__(self, host, port):
        self.es_host = host
        self.es_port = port

        self.es = None

    @classmethod
    def from_cralwer(cls, cralwer):
        return cls(host=cralwer.settings.ES_HOST, port=cralwer.settings.ES_PORT)

    def open_spider(self):
        self.es = Elasticsearch([{'host': self.es_host, 'port': self.es_port}])

    def close_spider(self):
        pass

    def process_item(self, item, spider):
        doc_id = item['ip'] + ':' + item['port']
        self.es.index(index='ippool', doc_type=item['protocol'], id=doc_id, body=item)
        return item