# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import requests
from ximalaya import  settings
class XimalayaPipeline(object):
    def process_item(self, item, spider):
        if item['mp3_url']:
            print ("------------"+item['mp3_url'])

            file_path=settings.FILE_STORE+"/"+item['title']+".m4a"

            with open(file_path, 'wb') as file_writer:
                # 下载图片
                conn = requests.get(item['mp3_url'])
                file_writer.write(conn.content)
            file_writer.close()
        return item
# class Storymp3Pipeline(object):
#     def __init__(self):
#         self.file = codecs.open('story_mp3_data.json',mode='wb',encoding='utf-8')
#
#     def process_item(self,item,spider):
#         line = json.dumps(dict(item)) + '\n'
#         self.file.write(line.decode("unicode_escape"))
#
#         return item
#
#     def spider_closed(self,spider):
#         self.file.close()