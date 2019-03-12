import requests
from bs4 import BeautifulSoup
import lxml
from multiprocessing import Process, Queue
import random
import json
import time
import requests
from lxml import etree

class Proxies(object):
    """docstring for Proxies"""

    def __init__(self, page = 10):
        self.proxies = []
        self.verify_pro = []
        self.page_end = page
        self.PROTOCOL = 'https'
        self.headers = {
            "Referer": "https://www.fitchratings.com/site/search?content=headlines",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
        }
        self.get_proxies()


    def decrypt(self,src):
        s = 'ABCDEFGHIZ'
        dst = ''
        for c in src:
            dst += str(s.find(c))
        dst = int(dst) >> 3
        return dst

    def get_proxies(self):
        page = 1
        while page < self.page_end:
            url = "http://www.data5u.com/free/gwpt/index.shtml"
            res = requests.get(url=url,
                               headers=self.headers)
            html = etree.HTML(res.text)
            ip_pool = html.xpath("//div[@class='wlist'][last()]/ul/li/ul[@class ='l2']")
            for cur_ip in ip_pool:
                Type = cur_ip.xpath("./span[4]//text()")[0].strip()
                if Type == self.PROTOCOL:
                    ip = cur_ip.xpath("./span[1]//text()")[0].strip()
                    src = cur_ip.xpath("./span[2]/li[contains(@class,'port')]/@class")[0].split()[1]
                    port = self.decrypt(src)  # 解密函数
                    self.proxies.append(f"{self.PROTOCOL}://{ip}:{port}")
            page += 1


    def verify_proxies(self):
        # 没验证的代理
        old_queue = Queue()
        # 验证后的代理
        new_queue = Queue()
        print('verify proxy........')
        works = []
        for _ in range(15):
            works.append(Process(target=self.verify_one_proxy, args=(old_queue, new_queue)))
        for work in works:
            work.start()
        for proxy in self.proxies:
            old_queue.put(proxy)
        for work in works:
            old_queue.put(0)
        for work in works:
            work.join()
        self.proxies = []
        while 1:
            try:
                self.proxies.append(new_queue.get(timeout=1))
            except:
                break
        print('verify_proxies done!')

    def verify_one_proxy(self, old_queue, new_queue):
        while 1:
            proxy = old_queue.get()
            if proxy == 0: break
            protocol = 'https' if 'https' in proxy else 'http'
            proxies = {protocol: proxy}
            try:
                if requests.get('http://www.baidu.com', proxies=proxies, timeout=2).status_code == 200:
                    print('success %s' % proxy)
                    new_queue.put(proxy)
            except:
                print('fail %s' % proxy)


if __name__ == '__main__':
    a = Proxies()
    a.verify_proxies()
    print(a.proxies)
    proxie = a.proxies
    with open('https_proxies.txt', 'a') as f:
        for proxy in proxie:
            f.write(proxy + '\n')