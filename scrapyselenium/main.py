import os
import sys

from scrapy.cmdline import execute

# 添加当前项目的绝对地址
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# print(os.path.dirname(os.path.abspath(__file__)))
# 执行 scrapy 内置的函数方法execute，使用 crawl 爬取并调试
execute(['scrapy', 'crawl', 'taobao'])
