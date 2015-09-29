#!/usr/bin/python
# -*- coding: utf-8 -*-

import scrapy
#import urlparse

from goods.items import ProductInfo
from goods.items import SkuInfo
from goods.items import GenderInfo

class alexandalexaGenderSpider(scrapy.Spider):
    name = "alexandalexa_gender"
    allowed_domains = ["alexandalexa.com"]
    start_urls = [
        "http://www.alexandalexa.com/burberry/s/110",
        "http://www.alexandalexa.com/il-gufo/s/486",
        "http://www.alexandalexa.com/ikks/s/485",
        "http://www.alexandalexa.com/stella-mccartney-kids/s/127",
        "http://www.alexandalexa.com/ilovegorgeous/s/887",
        "http://www.alexandalexa.com/ugg-australia/s/746",
        "http://www.alexandalexa.com/little-eleven-paris/s/546",
        "http://www.alexandalexa.com/adidas-originals/s/325",
        "http://www.alexandalexa.com/kenzo/s/119",
    ]

    def parse(self, response):
        #for article in response.xpath('//div[@class="product-list"]/article'):
        #response.xpath('//div[@data-property-type-id="13"]/div/a/@href').extract()
        for article in response.xpath('//div[@data-property-type-id="13"]/div/a'):
            href = article.xpath('@href').extract()[0]
            product_gender = article.xpath('text()').extract()[0].strip()
            product_url = response.urljoin(href)
            #这里只需要url  其它信息都从详情页拿
            #name = article.xpath('a/p[@class="name"]/text()').extract()[0]
            #price = article.xpath('a/p[contains(@class,"price")]/del/text()').extract()[0]
            #brand = article.xpath('a/p[@class="brand"]/text()').extract()[0]
            print product_url,product_gender
            request = scrapy.Request(product_url, callback=self.parse_product_detail)
            request.meta['product_url'] = product_url
            request.meta['product_gender'] = product_gender
            yield request
            break

        # 追踪翻页link
        #next_page = response.xpath('//div[@class="controls"]/a[@class="control next"]/@href')
        #if next_page:
        #    next_url = response.urljoin(next_page.extract()[0])
        #    yield scrapy.Request(next_url, self.parse)

    def parse_product_detail(self, response):
        product_url = response.meta['product_url']
        product_gender = response.meta['product_gender']
        #print "parse_product_detail = ",product_url,product_gender
        for article in response.xpath('//div[@class="product-list"]/article'):
            href = article.xpath('a/@href').extract()[0]
            url = response.urljoin(href)
            gender_info =  GenderInfo()
            gender_info['product_url'] = url
            gender_info['product_gender'] = product_gender
            print "product_detail = ",url
            yield gender_info
        # 追踪翻页link
        return
        next_page = response.xpath('//div[@class="controls"]/a[@class="control next"]/@href')
        if next_page:
            next_url = response.urljoin(next_page.extract()[0])
            print "next_url = ",next_url
            request = scrapy.Request(next_url, callback=self.parse_product_detail)
            request.meta['product_url'] = product_url
            request.meta['product_gender'] = product_gender
            yield request
            #yield scrapy.Request(next_url, self.parse_product_detail)
        return

