# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from xpinyin import Pinyin
from datetime import datetime
import pymysql

from zolProject.models.es_type import ArticleType
from zolProject.settings import MYSQL_HOST, MYSQL_PORT, MYSQL_CHARSET, MYSQL_DB, MYSQL_PASSWD, MYSQL_USER


class ZolprojectPipeline(object):
    # con = pymysql.connect(host=MYSQL_HOST, port=MYSQL_PORT, user=MYSQL_USER, passwd=MYSQL_PASSWD, db=MYSQL_DB,charset=MYSQL_CHARSET)
    # cur = con.cursor()
    pin = Pinyin()

    def process_item(self, item, spider):
        article = ArticleType()


        article.bookName = item['bookName']
        article.original = item['original']
        article.anchor = item['anchor']
        article.introduction = item['introduction']
        article.bookImg = item['bookImg']
        article.bookType = item['bookType']

        article.save()
        return item


def process_item_zol(self, item, spider):
    # brand = item['brand'][0]
    brand = item['brand'][0]

    # 手机价格
    phonePrice = item['phonePrice'][0]
    # 没有价格默认设置0
    if phonePrice.isdigit() == False:
        phonePrice = 0

    # 字符串处理手机中文
    brandNameChinese = brand.replace('（', '(')
    brandNameChinese = brandNameChinese.split('(')
    brandNameChinese = brandNameChinese[0]

    # 字符串处理手机拼音
    brandNamepinyin = brand.replace('（', '(')
    brandNamepinyin = brandNamepinyin.split('(')
    brandNamepinyin = brandNamepinyin[0]
    brandNamepinyin = self.pin.get_pinyin(brandNamepinyin, " ")

    # 将datatime类型的数据转换为字符串类型的数据，用%s插入到数据库中。
    createTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        sql = "INSERT INTO t_mobile_phone_brands (brand_name_chinese, brand_name_pinyin,brand_full_name, phone_price,create_time) VALUES ( '%s', '%s','%s', '%s','%s');" % (
            brandNameChinese, brandNamepinyin, brand, phonePrice, createTime)
    # self.cur.execute(sql)
    # self.con.commit()
    except Exception as  e:
        print(e)
        self.con.rollback()
