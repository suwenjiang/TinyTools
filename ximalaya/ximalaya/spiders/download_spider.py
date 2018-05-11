import scrapy
import json
from ximalaya.items import XimalayaItem
class XimalayaSpider(scrapy.Spider):
    name = "ximalaya"
    start_urls = [
        "http://www.ximalaya.com/81407276/album/10401275/",
    ]

    def parse(self, response):
        for sound_id  in response.css('li[sound_id]'):
            yield response.follow("/tracks/"+sound_id.css("a.title::attr(href)").extract_first().strip().split('/')[-2].strip()+".json",self.parse_sound)




        for href in response.css('.pagingBar_wrapper a[rel=next]::attr(href)'):

            yield response.follow(href, self.parse)


    def parse_sound(self, response):


        data=json.loads(response.body_as_unicode())
        item=XimalayaItem()
        item['mp3_url'] = data['play_path']
        item['title']=data['title']
        yield  item
