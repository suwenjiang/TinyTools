# coding:utf-8
__author__ = 'jiangmb'

import requests
from bs4 import BeautifulSoup
import  sys

reload(sys)
sys.setdefaultencoding('utf-8')

next_page_url='/r/search?q=gis&type=people&offset=0'
users_info_list=[]
while True:
        r = requests.get('https://www.zhihu.com'+next_page_url)

        next_page_url=r.json()['paging']['next']
        print (next_page_url)
        if len(next_page_url)!=0:
                content=r.json()['htmls']
                html_doc=''.join(content)
                soup = BeautifulSoup(html_doc, 'html.parser')
                user_info={}
                for link in soup.find_all('li'):
                        user_info['src']=link.find_all('a')[0].img['src']
                        user_info['id']=link.find_all('a')[1].string
                        user_info['href']=link.find_all('a')[1]['href']
                        # print user_info
                        user_info['answers']=link.find_all('a')[2].strong.string
                        user_info['posts']=link.find_all('a')[3].strong.string
                        user_info['followers']=link.find_all('a')[4].strong.string
                        users_info_list.append(user_info)
        else:
                print (users_info_list)
                break

