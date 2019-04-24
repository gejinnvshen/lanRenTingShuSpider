# lanRenTingShuSpider
爬取懒人听书平台书籍的书名、作者名、分类，后续还会增加爬取音频


爬虫用到的框架：scrapy
Anaconda是专注于数据分析的Python发行版本

scrapy简单入门及实例讲解：https://www.cnblogs.com/kongzhagen/p/6549053.html
scrapy进阶实例：https://blog.csdn.net/z564359805/article/details/80886382


scrapy框架知识点
```
`1、ROBOTSTXT_OBEY = False 粗解`
[https://www.jianshu.com/p/19c1ea0d59c2](https://www.jianshu.com/p/19c1ea0d59c2)
`2、爬虫-User-Agent和代理池`
[https://www.cnblogs.com/sunxiuwen/p/10112057.html](https://www.cnblogs.com/sunxiuwen/p/10112057.html)
`3、`
scrapy项目配置文件：
scrapy.cfg：爬虫项目的配置文件。
__init__.py：爬虫项目的初始化文件，用来对项目做初始化工作。 
items.py：爬虫项目的数据容器文件，用来定义要获取的数据。
1、pipelines.py：爬虫项目的管道文件，用来对items中的数据进行进一步的加工处理。 2、scrapy的pipeline是一个非常重要的模块，主要作用是将return的items写入到数据库、文件等持久化模块
settings.py：爬虫项目的设置文件，包含了爬虫项目的设置信息。 
middlewares.py：爬虫项目的中间件文件，

`4`
使用anaconda prompt运行.py文件，执行scrapy crwal xx指令时，xx是.py文件中给name赋的值
使用anaconda prompt运行.py文件，执行scrapy crwal xx指令时，如果报错说少了yy modules，直接输入pip install yy执行安装包，不用在进入对应的项目目录下
5、  [https://scrapy-chs.readthedocs.io/zh_CN/1.0/intro/tutorial.html?highlight=extract](https://scrapy-chs.readthedocs.io/zh_CN/1.0/intro/tutorial.html?highlight=extract)

*   [`xpath()`](https://scrapy-chs.readthedocs.io/zh_CN/1.0/topics/selectors.html#scrapy.selector.Selector.xpath "scrapy.selector.Selector.xpath"): 传入xpath表达式，返回该表达式所对应的所有节点的selector list列表 。
*   [`css()`](https://scrapy-chs.readthedocs.io/zh_CN/1.0/topics/selectors.html#scrapy.selector.Selector.css "scrapy.selector.Selector.css"): 传入CSS表达式，返回该表达式所对应的所有节点的selector list列表.
*   [`extract()`](https://scrapy-chs.readthedocs.io/zh_CN/1.0/topics/selectors.html#scrapy.selector.Selector.extract "scrapy.selector.Selector.extract"): 序列化该节点为unicode字符串并返回list。
*   [`re()`](https://scrapy-chs.readthedocs.io/zh_CN/1.0/topics/selectors.html#scrapy.selector.Selector.re "scrapy.selector.Selector.re"): 根据传入的正则表达式对数据进行提取，返回unicode字符串list列表。

6、elastisearch查询语句
[https://segmentfault.com/q/1010000017553309/](https://segmentfault.com/q/1010000017553309/)

7、
#传入xpath表达式，返回该表达式所对应的所有节点的selector list列表
#extract(): 返回被选择元素的unicode字符串
8、yield
# yield的作用   这里是在爬取完一页的信息后，我们在当前页面获取到了下一页的链接，然后通过 yield 发起请求，
                # 并且将 parse 自己作为回调函数来处理下一页的响应
                #  https://www.jianshu.com/p/7c1a084853d8
                yield Request(self.lrtsUrl + next_link, callback=self.parse, headers=headers)  #获取下一页，parse是回调函数来处理下一页的响应
9、meta  scrapy的request的meta参数是什么意思？
[https://blog.csdn.net/master_ning/article/details/80558985](https://blog.csdn.net/master_ning/article/details/80558985)


```

python基础知识点：
```
class:#创建类  类就是一个模板，模板里可以包含多个函数，函数里实现一些功能
def:#创建类中函数
pass:pass 不做任何事情，一般用做占位语句。
if __name__ == '__main__':的作用
[https://www.cnblogs.com/kex1n/p/5975575.html](https://www.cnblogs.com/kex1n/p/5975575.html)
5、python range() 函数可创建一个整数列表，一般用在 for 循环中。
函数语法
range(start, stop[, step])
6、Python len() 方法返回对象（字符、列表、元组等）长度或项目个数。
语法
len()方法语法：
len( s )
```


