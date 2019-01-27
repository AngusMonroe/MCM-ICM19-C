__author__ = 'XJX'
__date__ = '2017.07.19'

import re
import urllib.request
import urllib

# 网址
url1 = "https://www.nowmsg.com/us/"
url2 = "/all_city.asp"
state_list = ['Kentucky', 'Ohio', 'Pennsylvania', 'West Virginia', 'Virginia']
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                        'Chrome/51.0.2704.63 Safari/537.36'}

for state in state_list:
    url = url1 + urllib.request.quote(state) + url2
    print(url)
    req = urllib.request.Request(url=url, headers=headers, verify=False)
    res = urllib.request.urlopen(req)

    try:
        # 转换为utf-8码
        data = res.read()
        # print(data)
    except:
        continue
    print(data)
    break
    # 正则表达式提取页面中所有队列, 并判断是否已经访问过, 然后加入待爬队列
    # linkre1 = re.compile("<div class=\"well\">")
    # for x in linkre1.findall(data):  ##返回所有有匹配的列表
