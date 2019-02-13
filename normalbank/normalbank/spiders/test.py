import requests

# 使用代理获取百度首页
headers = {
  "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"
}
#  定义代理的字典
proxies = {
  # "http":"http://14.118.252.64:6666"
  # "https":"https://114.99.30.126:18118"
  "http": "http://200.233.134.85:8521"
}

# 使用代理给服务器发送请求
response = requests.get("http://icanhazip.com/", proxies=proxies, headers=headers,timeout = 15)
# 获取状态
print(response.status_code)
print(response.content.decode())