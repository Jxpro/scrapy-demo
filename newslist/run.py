import sys

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from newslist.utlis import get_config


def run():
    name = sys.argv[1]
    # 获取配置文件名称
    custom_settings = get_config(name)
    # 获取爬虫名称
    spider = custom_settings.get('spider', 'universal')
    # 获取项目配置
    project_settings = get_project_settings()
    # 合并配置
    settings = dict(project_settings)
    settings.update(custom_settings.get('settings'))
    # 启动爬虫
    process = CrawlerProcess(settings)
    process.crawl(spider, name=name)
    process.start()


if __name__ == '__main__':
    run()
