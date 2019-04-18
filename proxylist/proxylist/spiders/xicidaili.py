# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
from scrapy.spiders import CrawlSpider

from proxylist.proxylist.items import IPlistItem


def parse_ip_list(response):
    item = IPlistItem()
    html_ip_list = response.css('#ip_list').get()
    soup = BeautifulSoup(html_ip_list, 'html.parser')
    return item


class XicidailiSpider(CrawlSpider):
    name = 'xicidaili'
    allowed_domains = ['xicidaili.com']
    start_urls = ['https://www.xicidaili.com/nn']

    current_page = 1

    def parse(self, response):
        self.parse_pagination(response)
        return parse_ip_list(response)

    def parse_pagination(self, response):
        html_pagination = response.css('.pagination').get()
        soup = BeautifulSoup(html_pagination, 'html.parser')

        total_pages = soup.select('.next_page')[0].find_previous_sibling().get_text()

        self.logger.info(total_pages)

        self.current_page = self.current_page + 1
        if self.current_page < int(total_pages):
            scrapy.Request('https://www.xicidaili.com/nn/%i' % self.current_page, self.parse)
            self.logger.info('https://www.xicidaili.com/nn/%i' % self.current_page)
