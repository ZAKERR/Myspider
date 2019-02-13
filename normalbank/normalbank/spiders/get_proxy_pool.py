from lxml import etree
import requests



HEADERS = {
    "Content-Type": "application/json",
    "Referer": "https://www.fitchratings.com/site/search?content=headlines",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
}

PROTOCOL = 'https'

def decrypt(src):
    s = 'ABCDEFGHIZ'
    dst = ''
    for c in src:
        dst += str(s.find(c))
    dst = int(dst) >> 3
    return dst

def get_pool():
    url = "http://www.data5u.com/free/gwpt/index.shtml"
    res = requests.get(url=url,
                       headers = HEADERS)

    html = etree.HTML(res.text)
    ip_pool = html.xpath("//div[@class='wlist'][last()]/ul/li/ul[@class ='l2']")
    sat_ip = []  #满足https的代理ip
    for cur_ip in ip_pool:
        Type = cur_ip.xpath("./span[4]//text()")[0].strip()
        if Type == PROTOCOL:
            ip = cur_ip.xpath("./span[1]//text()")[0].strip()
            src = cur_ip.xpath("./span[2]/li[contains(@class,'port')]/@class")[0].split()[1]
            port = decrypt(src)
            sat_ip.append(f"{PROTOCOL}://{ip}:{port}")
    return sat_ip

# def test_rate():
#     to_url = "https://www.brookings.edu/search/?post_type=post&post_type=bpea-article&post_type=research&post_type=testimony&orderby=date"
#     # to_url = "http://icanhazip.com/"
#     time = 0    #所有有效代理ip访问的请求响应的总时间
#     eff_num = 0 #在规定时间内访问的有效代理ip个数
#     fail_ip = []
#     ip_list = get_pool()
#     for cur_ip in ip_list:
#         print(cur_ip)
#         try:
#             proxies = {}
#             proxies[PROTOCOL] = cur_ip
#             res = requests.get(url=to_url,proxies = proxies,headers = HEADERS,verify = False,timeout = 20)
#             if res.status_code == 200:
#                 eff_num += 1
#                 time += res.elapsed.total_seconds()
#         except requests.exceptions.Timeout as e:
#                 print(e)
#         except requests.exceptions.HTTPError as e:
#                 print(e)
#         except:
#             continue
#
#     return [eff_num,time,len(ip_list)]
#
# if __name__ == '__main__':
#     record = test_rate()
#     print(record[0],record[1],record[2])
