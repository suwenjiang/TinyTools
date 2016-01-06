#coding:utf-8
__author__ = 'jiangmb'
import requests
from bs4 import BeautifulSoup
#从自己的网站中获取sitemap.xml
sitemap=requests.get('http://gishub.info/sitemap.xml')
urls=[]
if sitemap.status_code==200:
    # print sitemap.text
    soup=BeautifulSoup(sitemap.text,'xml')
    tags = soup.find_all("loc")
    urls += [x.string for x in tags]
    urls = set(urls)  # 先去重
    print("%s url need to submit " % len(urls))
    data = "\n".join(urls)
    print data
    url = "your own baidu url"

    print  requests.post(url, data=data).text
