# -*- coding: UTF-8 -*-
import sys

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from proxylist.spiders.xicidaili import XicidailiSpider


def main(argv):
    process = CrawlerProcess(get_project_settings())

    process.crawl(XicidailiSpider)
    process.start()  # the script will block here until the crawling is finished


if __name__ == '__main__':
    sys.exit(main(sys.argv))
