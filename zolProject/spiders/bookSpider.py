# -*- coding: utf-8 -*-
import random

from scrapy import Selector, Request  #基于select模块实现的IO多路复用，建议大家使用
import logging

from scrapy.spiders import CrawlSpider
from zolProject.items import BookItems    # 导入item中结构化数据模板  zolProject是项目名
from zolProject.settings import USER_AGENTS, headers

logger = logging.getLogger(__name__)  #指定name，返回一个名称为name的Logger实例

#创建类  类就是一个模板，模板里可以包含多个函数，函数里实现一些功能
class BookSpider(CrawlSpider):
    # 爬虫名称，唯一
    name = "book"
    # 允许访问的域
    allow_domains = ["www.lrts.me"]
    lrtsUrl = "http://www.lrts.me"
    # 初始URL
    start_urls = [
        "http://www.lrts.me/book/category/83",            #如果start_urls里多个链接例如（"http://www.lrts.me/book/category/3059","http://www.lrts.me/book/category/16"），那爬虫顺序是先爬完第一个在爬接下来的链接。好像可以写个脚本专门来获取所有tab的跳转链接，然后赋值给start_urls
        "http://www.lrts.me/book/category/9054",
        "http://www.lrts.me/book/category/9056",
        "http://www.lrts.me/book/category/9052",
        "http://www.lrts.me/book/category/9053",
        "http://www.lrts.me/book/category/9055",
        "http://www.lrts.me/book/category/9058",
        "http://www.lrts.me/book/category/71",
        "http://www.lrts.me/book/category/87"
    ]
    #创建类中函数
    #parse() 是spider的一个方法。 被调用时，每个初始URL完成下载后生成的 Response 对象将会作为唯一的参数传递给该函数。
    # 该方法负责解析返回的数据(response data)，提取数据(生成item)以及生成需要进一步处理的URL的 Request 对象
    def parse(self, response):
        print("上")
        print(response)   #<200 http://www.lrts.me/book/category/3085>  <200 http://www.lrts.me/book/category/3085/recommend/5/20> response对象有很多基础参数https://blog.csdn.net/on_the_road_2018/article/details/80981222
        sel = Selector(response)
        print("下")
        parentTitle = response.xpath('//section[@class="category-filter"]/div/a[@class="active"]/text()').extract()
        print(sel)   #<Selector xpath=None data='<html lang="zh-CN">\r\n<head>\r\n    <title>'>
        print(parentTitle)
        print("标签")
        #Scrapy提取数据有自己的一套机制。它们被称作选择器(seletors)，因为他们通过特定的 XPath 或者 CSS 表达式来“选择” HTML文件中的某个部分
        sites = sel.xpath('//div[@class="category-book"]/ul/li')   #传入xpath表达式，返回该表达式所对应的所有节点的selector list列表
        logger.warning("=============")
        print(sites)
        logger.warning("==============")
        for site in sites:
            item = BookItems()

            bookName = site.xpath('div[@class="book-item-r"]/a[@class="book-item-name"]/text()').extract()  #extract(): 返回被选择元素的unicode字符串列表 https://scrapy-chs.readthedocs.io/zh_CN/0.24/topics/selectors.html#selectorlist
            logger.info(bookName)
            print(bookName)    #得到的结果是数组
            print("bookname")
            original = site.xpath('div/div/a[@class="author"]/text()').extract()
            logger.info(original)

            anchor = site.xpath('div/div/a[@class="g-user"]/text()').extract()
            logger.info(anchor)

            introduction = site.xpath('div[@class="book-item-r"]/p/text()').extract()
            logger.info(introduction)

            bookImg = site.xpath('div/a/img/@src').extract()
            logger.info(bookImg)

            item['bookName'] = bookName
            item['original'] = original
            item['anchor'] = anchor
            item['introduction'] = introduction
            item['bookImg'] = bookImg
            item['bookType'] = parentTitle

            yield item    #我们将在 pipelines.py里将传递过来的 scrapy.Item 对象保存到数据库里去   yield的作用https://www.jianshu.com/p/7c1a084853d8

        next_name = sel.xpath('//div[@class="pager"]/div/a[@class="next"]/text()').extract_first()   #extract_first()提取到第一个匹配到的元素
        print(next_name + "下一个名字")
        if next_name == "下一页":    #意思是还有下一页没爬取,接着爬取
            next_link = sel.xpath('//div[@class="pager"]/div/a[@class="next"]/@href').extract_first()   #提取到第一个匹配到的元素 https://scrapy-chs.readthedocs.io/zh_CN/1.0/topics/selectors.html?highlight=extract_first
            logger.info("是否获取到下一页链接地址:"+self.lrtsUrl + next_link)  #只执行了一次
            print(next_link)   #/book/category/3085/recommend/3/20   下一页的url
            if next_link:
                print("下一页的url")
                useragent = random.choice(USER_AGENTS)     #随机生成一个useragent
                headers['User-Agent'] = useragent

                # yield的作用   这里是在爬取完一页的信息后，我们在当前页面获取到了下一页的链接，然后通过 yield 发起请求，
                # 并且将 parse 自己作为回调函数来处理下一页的响应
                #  https://www.jianshu.com/p/7c1a084853d8
                yield Request(self.lrtsUrl + next_link, callback=self.parse, headers=headers)  #获取下一页，parse是回调函数来处理下一页的响应