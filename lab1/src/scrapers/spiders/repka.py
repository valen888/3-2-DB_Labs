# -*- coding: utf-8 -*-
from scrapy.http.response import Response
import scrapy


class RepkaSpider(scrapy.Spider):
    name = 'uamade'
    start_urls = ['https://repka.ua/products/smartfony/?brands=105&serija_smart=124817']

    def parse(self, response: Response):
        products = response.xpath("//div[contains(@class, 'ypi-grid-list__item_body')]")[:20]
        for product in products:
            yield {
                'description': product.xpath(".//a[@class='product-item-name']/@title").get(),
                'price': product.xpath(".//span[@class='price']/text()").get(),
                'img': product.xpath(".//img[@class='owl-lazy mousedown']/@src").get()
            }
