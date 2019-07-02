# -*- coding: utf-8 -*-
import scrapy
from bhunew_spider.items import BhunewSpiderItem
import re


class BhuNewSpider(scrapy.Spider):
    name = 'bhu_new'
    allowed_domains = ['www.bhu.edu.cn/page/list.asp?boardid=bd_news']
    start_urls = ['http://www.bhu.edu.cn/page/list.asp?boardid=bd_news&page=1']

    def start_requests(self):
        reqs = []
        for i in range(1, 204):
            req = scrapy.Request(
                "http://www.bhu.edu.cn/page/list.asp?boardid=bd_news&page=%s" % i)
            reqs.append(req)
        return reqs

    def parse(self, response):
        re_str = '^v.*'
        for href in response.xpath('//a/@href').extract():
            match_obj = re.match(re_str, href)
            if match_obj:
                item = BhunewSpiderItem()
                url = "http://www.bhu.edu.cn/page/" + match_obj.group()
                yield scrapy.Request(url=url, meta={'item': item}, callback=self.detial_parse, dont_filter=True)

    def detial_parse(self, response):
        item = response.meta['item']
        # re_str = '^s.*'
        # img_Path = 'C:\\Users\\Administrator\\Desktop\\bhunew_spider\\bhunew_spider\\spiders\\img\\'
        item['title'] = response.xpath('//b/text()').extract()
        item['time'] = response.xpath('//div[2]/text()').extract()
        item['content'] = response.xpath('//div[4]/text()').extract()
        item['people'] = response.xpath('//td[@align="center"]/text()').extract()[6]
        # for img in response.xpath('//a/img/@src').extract():
        #     match_obj = re.match(re_str, img)
        #     if match_obj:
        #         item['img_url'] = "http://www.bhu.edu.cn/page/" + match_obj.group()
        #         '''
        #         img_url = "http://www.bhu.edu.cn/page/" + match_obj.group()
        #         res = urllib2.urlopen(img_url)
        #         name = str(match_obj.group()) + '.jpg'
        #         with open(img_Path+name, 'wb') as f:
        #             f.write(res.read())
        #         '''
        yield item
