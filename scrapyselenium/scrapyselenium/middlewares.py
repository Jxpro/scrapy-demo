# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import json
from logging import getLogger

from scrapy import signals
from scrapy.http import HtmlResponse
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait


# useful for handling different item types with a single interface


class ScrapyseleniumSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class ScrapyseleniumDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    def __init__(self, timeout=None, cookie_list=None):
        self.logger = getLogger(__name__)
        self.timeout = timeout
        self.browser = Chrome()
        self.wait = WebDriverWait(self.browser, self.timeout)
        self.cookie_list = cookie_list

        self.browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """Object.defineProperty(navigator, 'webdriver', {get: () => false})""",
        })

        self.browser.get('https://s.taobao.com')
        for cookie in self.cookie_list:
            if cookie.get('domain') != '.taobao.com':
                # print('------------------- unmatched domain ----------------------------')
                # print(cookie.get('domain'))
                # print('-----------------------------------------------------------------')
                continue
            cookie['sameSite'] = 'Strict'
            self.browser.add_cookie(cookie)
        print('-----------------------------------------------------------------')
        self.logger.debug('cookies added!!!')
        print('-----------------------------------------------------------------')

    # 该方法未被调用
    # 原因可能是由 HtmlResponse 所导致
    def __del__(self):
        self.browser.close()
        self.logger.debug('--------------------------------------------------------------')
        self.logger.debug('chrome closed !!! ')
        self.logger.debug('--------------------------------------------------------------\n\n\n\n\n\n\n\n\n\n\n')

    @classmethod
    def from_crawler(cls, crawler):
        cookie_list = json.load(open(crawler.settings.get('BOT_NAME') + '/cookie.json'))
        # print(cookie_list)
        return cls(timeout=crawler.settings.get('SELENIUM_TIMEOUT'), cookie_list=cookie_list)

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        """
            用selenium抓取页面
            :param request: Request对象
            :param spider: Spider对象
            :return: HtmlResponse
        """
        self.logger.debug('Chrome is Starting')
        page = request.meta.get('page', 0) + 1
        try:
            if request.url not in self.browser.current_url:
                self.browser.get(request.url)

            if page > 1:
                input_page = self.wait.until(
                    ec.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-pager div.form > input')))
                submit = self.wait.until(
                    ec.element_to_be_clickable((By.CSS_SELECTOR, '#mainsrp-pager div.form > span.btn.J_Submit')))
                input_page.clear()
                input_page.send_keys(page)
                submit.click()
            self.wait.until(
                ec.text_to_be_present_in_element((By.CSS_SELECTOR, '#mainsrp-pager li.item.active > span'), str(page)))
            self.wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-itemlist .items .item')))
            return HtmlResponse(url=request.url, body=self.browser.page_source, request=request, encoding='utf-8',
                                status=200)
        except TimeoutException:
            return HtmlResponse(url=request.url, status=500, request=request)

    # def process_response(self, request, response, spider):
    #     # Called with the response returned from the downloader.
    #
    #     # Must either;
    #     # - return a Response object
    #     # - return a Request object
    #     # - or raise IgnoreRequest
    #     return response

    # def process_exception(self, request, exception, spider):
    #     # Called when a download handler or a process_request()
    #     # (from other downloader middleware) raises an exception.
    #
    #     # Must either:
    #     # - return None: continue processing this exception
    #     # - return a Response object: stops process_exception() chain
    #     # - return a Request object: stops process_exception() chain
    #     pass
    #
    # def spider_opened(self, spider):
    #     spider.logger.info('Spider opened: %s' % spider.name)
