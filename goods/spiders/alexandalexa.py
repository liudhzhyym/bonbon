#!/usr/bin/python
# -*- coding: utf-8 -*-

import scrapy
#import urlparse

from goods.items import ProductInfo
from goods.items import SkuInfo

class alexandalexaBurberrySpider(scrapy.Spider):
    name = "alexandalexa"
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
        #logo_name = response.url.split("/")[-3]
        #print logo_name
        for article in response.xpath('//div[@class="product-list"]/article'):
            href = article.xpath('a/@href').extract()[0]
            product_url = response.urljoin(href)
            #这里只需要url  其它信息都从详情页拿 
            #name = article.xpath('a/p[@class="name"]/text()').extract()[0]
            #price = article.xpath('a/p[contains(@class,"price")]/del/text()').extract()[0]
            #brand = article.xpath('a/p[@class="brand"]/text()').extract()[0]

            request = scrapy.Request(product_url, callback=self.parse_product_detail)
            request.meta['product_url'] = product_url
            print "product_url = ",product_url
            #request.meta['logo_name'] = logo_name
            yield request
            break

        # 追踪翻页link
        #next_page = response.xpath('//div[@class="controls"]/a[@class="control next"]/@href')
        #if next_page:
        #    next_url = response.urljoin(next_page.extract()[0])
        #    yield scrapy.Request(next_url, self.parse)

        

    def parse_product_detail(self, response):
        product_url = response.meta['product_url']

        brand = response.xpath('//h1/a[@class="brand"]/text()').extract()[0].strip()
        name = response.xpath('//div[@class="product-info c-3"]/p[@class="name"]/text()').extract()[0].strip()
        from_price = response.xpath('//div[@class="product-info c-3"]/p[contains(@class,"price")]/del/text()').extract()[0].strip()
        from_price_selling = response.xpath('//div[@class="product-info c-3"]/p[contains(@class,"price")]/span[2]/text()').extract()[0].strip()
        # 页面不统一 attr可能混写在这个P区块 
        #product_detail = response.xpath('//section[@class="long-desc"]/p/text()').extract()[0].strip()

        # 跳过第一个是详情的P区块 
        #for attr in response.xpath('//section[@class="long-desc"]/p[not(@class="product-artno") and position() > 1]'):
        #    detail = attr.xpath(".//text()").extract()[0].strip()
        attr_list = []
        for attr in response.xpath('//section[@class="long-desc"]/p[not(@class="product-artno")]/text()'):
            detail = attr.extract().strip()
            if detail:
                attr_list.append(detail)
        product_detail = attr_list[0]
        attr_list.pop(0)

        product_id = response.xpath('//section[@class="long-desc"]/p[@class="product-artno"]/span/text()').extract()[0].strip()
            
        # 图片列表 
        pic_list = []
        for pic in response.xpath('//div[@class="thumbnails row"]/img'):
            zoom_url = pic.xpath("@data-zoom-src").extract()[0].strip()
            pic_list.append(zoom_url)

        # 属性值 
        type_list = []
        for type in response.xpath('//div[@class="property-list"]/a'):
            type = type.xpath("text()").extract()[0].strip()
            type_list.append(type)
            
        product =  ProductInfo()
        product['product_url'] = product_url
        product['product_name'] = name
        product['product_detail'] = product_detail
        product['from_price'] = from_price
        product['from_price_selling'] = from_price_selling
        product['brand'] = brand
        product['product_type'] = type_list
        product['product_tag'] = attr_list
        product['product_id'] = product_id
        product['product_pic'] = pic_list

        #sku_price_list = [" ".join(x.split()) for x in response.xpath('//select[@name="id"]/option[position()>1]/text()').extract()]
        # 从下拉选择信息中获取sku的价格 库存  
        size_list = []
        for option in  response.xpath('//select[@name="id"]/option[@data-units-for-sale]'):
            # eg."2 years - $909.00" 
            # or "2 month" 注意, 如果没有price, 则价格为from_price_selling
            size_and_price = " ". join(option.xpath("text()").extract()[0].split())
            size_and_price_list = size_and_price.split(" - ")
            size = size_and_price_list[0]
            size_list.append(size)
            size_price = from_price_selling
            if (len(size_and_price_list) == 2):
                size_price = size_and_price_list[1]

            # 库存 
            stock = option.xpath("@data-units-for-sale").extract()[0].strip()

            sku = SkuInfo()
            sku["brand"] = brand
            sku["product_id"] = product_id
            sku["size"] = size
            sku["sell_price"] = size_price
            sku["stock"] = stock
            yield sku


        product['product_size'] = size_list
        #yield product
        return
