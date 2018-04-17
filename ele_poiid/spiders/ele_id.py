# -*- coding: utf-8 -*-
import scrapy
from ele_poiid.ponits import city_point
from ele_poiid.items import ElePoiidItem
import  mzgeohash
import  json

class EleIdSpider(scrapy.Spider):
    name = 'ele_id'
    allowed_domains = ['www.ele.me']
    start_url = 'https://www.ele.me/restapi/shopping/restaurants?extras%5B%5D=activities&geohash={}&latitude={}&limit=24&longitude={}&offset={}'

    def start_requests(self):
        for i,j in city_point():
        #i=116.48105
        #j=39.996794
            for num in range(0, 960, 24):
                g = mzgeohash.encode(round(j, 5), round(i, 4))
                url = self.start_url.format(g[:11],round(j,6),round(i,6),num)
                yield scrapy.Request(url=url, callback=self.parse, )

    def parse(self, response):
        data = response.text
        jdata = json.loads(data)
        item = ElePoiidItem()
        for data_item in jdata:
            item['poi_id'] = data_item['id']
            item['name'] = data_item['name']
            item['address'] = data_item['address']

            yield item

