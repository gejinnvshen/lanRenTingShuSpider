# -*- coding:utf-8 -*-
# 数据类型
from elasticsearch_dsl import DocType, Date, Keyword, Text, Completion
# 引入链接函数
from elasticsearch_dsl.connections import connections


connections.create_connection(hosts="xxx")  #xxx是elasticsearch搭建的数据库的地址


class ArticleType(DocType):
    # 文章类型
   # bookName = Text()
   # original =  Text()
   # anchor =  Text()
   # introduction =  Text()
   # bookImg =  Text()

    class Index:
        name = 'lrts_book'    #给name赋值不能有大写
        settings = {
            "number_of_shards": 5,   #一旦索引创建完成，分片数量（number_of_shards）是不能修改的，副本数量（number_of_replicas）是可以修改的
        }

    class Meta:   #设置索引名称和表名称
        index = "lrts_book"
        doc_type = "category"


if __name__ == '__main__':  #https://www.cnblogs.com/kex1n/p/5975575.html
    ArticleType.init()
