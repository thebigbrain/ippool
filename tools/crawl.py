# -*- coding: UTF-8 -*-
import sys

from scrapy.crawler import CrawlerProcess

from proxylist.spiders.xicidaili import XicidailiSpider


class UserAgent:
    chrome = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) ' \
             'Chrome/73.0.3683.103 Safari/537.36'


def main(argv):
    process = CrawlerProcess({
        'USER_AGENT': UserAgent.chrome
    })

    process.crawl(XicidailiSpider)
    process.start()  # the script will block here until the crawling is finished


if __name__ == '__main__':
    sys.exit(main(sys.argv))
