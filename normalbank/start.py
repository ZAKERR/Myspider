from scrapy import cmdline
import os
import scrapy
from scrapy.crawler import CrawlerProcess
from normalbank.spiders.fitch import FitchSpider
from normalbank.spiders.mckinsey import MckinseySpider
from normalbank.spiders.weforum import WeforumSpider
from normalbank.spiders.spglobal import SpglobalSpider
from normalbank.spiders.moody import MoodySpider
from normalbank.spiders.bis import BisSpider
from normalbank.spiders.imf import ImfSpider
from normalbank.spiders.worldbank import WorldbankSpider
from normalbank.spiders.bruegel import BruegelSpider
from normalbank.spiders.brookings import BrookingsSpider
import time
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor

# def start_spider():
#     with open('scrapy_time.txt', "r", encoding='utf-8') as fn:
#         times = fn.read()
#
#     times = int(times) + 1
#     with open('scrapy_time.txt', "w", encoding='utf-8') as fn:
#         fn.write(str(times))
#
#     runner = scrapy.crawler.CrawlerRunner(settings = get_project_settings())
#     runner.crawl(FitchSpider)
#     runner.crawl(MckinseySpider)
#     runner.crawl(WeforumSpider)
#     runner.crawl(SpglobalSpider)
#     runner.crawl(MoodySpider)
#     runner.crawl(BisSpider)
#     runner.crawl(WorldbankSpider)
#     runner.crawl(BrookingsSpider)
#     runner.crawl(WorldbankSpider)
#     runner.crawl(BruegelSpider)



def start_spider():
    os.system("python D:/PYTHON_PRACTISE/综合练习/爬虫练习/Scrapy/normalbank/https_proxies.py")
    os.system("python D:/PYTHON_PRACTISE/综合练习/爬虫练习/Scrapy/normalbank/http_proxies.py")

    with open('scrapy_time.txt', "r", encoding='utf-8') as fn:
        times = fn.read()

    times = int(times) + 1
    with open('scrapy_time.txt', "w", encoding='utf-8') as fn:
        fn.write(str(times))

    runner = scrapy.crawler.CrawlerRunner(settings = get_project_settings())
    runner.crawl(FitchSpider)
    runner.crawl(MckinseySpider)
    runner.crawl(WeforumSpider)
    runner.crawl(SpglobalSpider)
    runner.crawl(MoodySpider)

    runner.crawl(BisSpider)
    runner.crawl(WorldbankSpider)
    runner.crawl(BrookingsSpider)
    runner.crawl(WorldbankSpider)
    runner.crawl(BruegelSpider)
    d = runner.join()
    d.addBoth(lambda _: reactor.stop())
    reactor.run()

#
#
# if __name__ == '__main__':
#     while True:
#         start_spider()
#         fir = 1
#         print("第{}次执行".format(fir))
#         fir = fir+1
#         time.sleep(10)

if __name__ == '__main__':
     start_spider()
#
#     from scrapy import cmdline
#     cmdline.execute("scrapy crawl fitch".split())
# os.system("python D:/PYTHON_PRACTISE/综合练习/爬虫练习/Scrapy/normalbank/https_proxies.py")
# time.sleep(5)
# os.system("python D:/PYTHON_PRACTISE/综合练习/爬虫练习/Scrapy/normalbank/http_proxies.py")
# time.sleep(5)
# cmdline.execute("scrapy crawl worldbank".split())
