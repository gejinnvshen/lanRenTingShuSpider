# -*- coding: utf-8 -*-
import random
import time

from scrapy import Selector, Request
import scrapy
import logging

from scrapy.spiders import CrawlSpider, Rule
from zolProject.items import ZolprojectItem, ZolTitlelink
from zolProject.settings import USER_AGENTS, headers

logger = logging.getLogger(__name__)


class PhoneSpider(CrawlSpider):
    name = "zol"
    allow_domains = ["detail.zol.com.cn"]
    zolUrl = "http://detail.zol.com.cn"

    start_urls = [
        "http://detail.zol.com.cn/cell_phone_index/subcate57_list_1.html"
    ]

    def parse(self, response):
        sel = Selector(response)
        sites = sel.xpath('//ul[@id="J_PicMode"]/li')

        for site in sites:
            item = ZolprojectItem()
            brand = site.xpath('h3/a/text()').extract()
            phonePrice = site.xpath('div/span/b[@class="price-type"]/text()').extract()
            item['brand'] = brand
            item['phonePrice'] = phonePrice
            yield item

        next_name = sel.xpath(
            '//div[@class="wrapper clearfix"]/div[@class="content"]/div[@class="page-box"]/div/a[@class="next"]/text()').extract_first()
        if next_name == "下一页":
            next_link = sel.xpath(
                '//div[@class="wrapper clearfix"]/div[@class="content"]/div[@class="page-box"]/div/a[@class="next"]/@href').extract_first()
            if next_link:
                useragent = random.choice(USER_AGENTS)
                headers['User-Agent'] = useragent
                time.sleep(1)
                yield Request(self.zolUrl + next_link, callback=self.parse, headers=headers)
        else:
            next_historyStart_number = sel.xpath(
                '//div[@class="wrapper clearfix"]/div[@class="content"]/div[@class="page-box"]/div/a[@class="historyStart"]/text()').extract_first()
            if next_historyStart_number == '41':
                next_historyStart = sel.xpath(
                    '//div[@class="wrapper clearfix"]/div[@class="content"]/div[@class="page-box"]/div/a[@class="historyStart"]/@href').extract_first()
                if next_historyStart:
                    useragent = random.choice(USER_AGENTS)
                    headers['User-Agent'] = useragent
                    time.sleep(1)
                    yield Request(self.zolUrl + next_historyStart, callback=self.parse, headers=headers)
            else:
                next_name = sel.xpath(
                    '//div[@class="wrapper clearfix"]/div[@class="content"]/div[@class="page-box"]/div/a[@class="next"]/text()').extract_first()
                if next_name == "下一页":
                    next_link = sel.xpath(
                        '//div[@class="wrapper clearfix"]/div[@class="content"]/div[@class="page-box"]/div/a[@class="next"]/@href').extract_first()
                    if next_link:
                        useragent = random.choice(USER_AGENTS)
                        headers['User-Agent'] = useragent
                        time.sleep(1)
                        yield Request(self.zolUrl + next_link, callback=self.parse, headers=headers)

        # def parse(self, response):
    #     selBrand = Selector(response)
    #     # 首先获取所有手机品牌
    #     items = []
    #     paramBrandUrls = selBrand.xpath('//div[@id="J_ParamBrand"]/a/@href').extract()
    #     for i in paramBrandUrls:
    #         item = ZolTitlelink()
    #         item['link'] = i
    #         items.append(item)
    #     for item in items:
    #         yield Request(self.zolUrl + item['link'], meta={'item': item}, callback=self.parse_detail, dont_filter=True)

    # def parse(self, response):
    #     sel = Selector(response)
    #     sites = sel.xpath('//ul[@id="J_PicMode"]/li')
    #
    #     for site in sites:
    #         item = ZolprojectItem()
    #         brand = site.xpath('h3/a/text()').extract()
    #         phonePrice = site.xpath('div/span/b[@class="price-type"]/text()').extract()
    #         item['brand'] = brand
    #         item['phonePrice'] = phonePrice
    #         yield item
    #
    #     next_link = sel.xpath(
    #         '//div[@class="wrapper clearfix"]/div[@class="content"]/div[@class="page-box"]/div/a[@class="next"]/@href').extract()
    #     if next_link:
    #         next_link = next_link[0]
    #         useragent = random.choice(USER_AGENTS)
    #         headers['User-Agent'] = useragent
    #         yield Request(self.zolUrl + next_link, callback=self.parse, headers=headers)
