# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
from scrapy.spiders import CrawlSpider

from proxylist.items import IPlistItem

demo_tr = '''
<tr class="odd">
<td class="country"><img alt="Cn" src="//fs.xicidaili.com/images/flag/cn.png"/></td>
<td>119.102.24.141</td>
<td>9999</td>
<td>
<a href="/2019-03-28/hubei">湖北武汉</a>
</td>
<td class="country">高匿</td>
<td>HTTPS</td>
<td class="country">
<div class="bar" title="0.113秒">
<div class="bar_inner fast" style="width:89%">
</div>
</div>
</td>
<td class="country">
<div class="bar" title="0.022秒">
<div class="bar_inner fast" style="width:96%">
</div>
</div>
</td>
<td>22天</td>
<td>19-04-19 09:00</td>
</tr>
'''


def parse_ip_list(response):
    html_ip_list = response.css('#ip_list').get()
    soup = BeautifulSoup(html_ip_list, 'html.parser')
    items = []
    for tr in soup.find_all('tr')[1:]:
        td = tr.find_all('td')
        item = IPlistItem()
        item['ip'] = td[1].get_text()
        item['port'] = td[2].get_text()
        item['location'] = td[3].get_text().replace('\n', '')
        item['protocol'] = td[5].get_text()
        items.append(item)
    return items


class XicidailiSpider(CrawlSpider):
    name = 'xicidaili'
    allowed_domains = ['xicidaili.com']
    start_urls = ['https://www.xicidaili.com/nn']

    current_page = 1
    total_pages = 0

    def parse(self, response):
        ip_list = parse_ip_list(response)
        for item in ip_list:
            yield item

        has_more = self.parse_pagination(response)
        if has_more:
            yield scrapy.Request('https://www.xicidaili.com/nn/%i' % self.current_page, self.parse)

    def parse_pagination(self, response):
        html_pagination = response.css('.pagination').get()
        soup = BeautifulSoup(html_pagination, 'html.parser')

        if not self.total_pages:
            self.total_pages = int(soup.select('.next_page')[0].find_previous_sibling().get_text())

        self.current_page = self.current_page + 1
        return self.current_page < self.total_pages
