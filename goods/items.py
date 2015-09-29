# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topecs/items.html

import scrapy


# 商品级别的信息 
class ProductInfo(scrapy.Item):
    # define the fields for your item here like:
    # 详情url 
    product_url = scrapy.Field()
    ########### 基础 
    # 商品名 
    product_name = scrapy.Field()
    # 商品介绍 
    product_detail = scrapy.Field()
    # 最低价格 
    from_price = scrapy.Field()
    # 当前销售的最低价格
    from_price_selling = scrapy.Field()

    ########### 属性 
    # 品牌 
    brand = scrapy.Field()
    # 分类 二级分类 上衣 T恤 
    product_type = scrapy.Field()
    # 年龄 2year 
    product_size = scrapy.Field()
    # 性别 男童 女童 baby 
    product_gender = scrapy.Field()
    # 标签 有机棉.. 
    product_tag = scrapy.Field()
    # ID
    product_id = scrapy.Field()
    # pic
    product_pic = scrapy.Field()


# sku级别信息 1个型号1个sku 
class SkuInfo(scrapy.Item):
    brand = scrapy.Field()
    # 关联product 
    product_id = scrapy.Field()
    # 现价 
    sell_price = scrapy.Field()
    ########### 属性 
    # 商品型号 xl xxl
    size = scrapy.Field()
    # 商品是否有库存 
    stock = scrapy.Field()


# 性别信息 
class GenderInfo(scrapy.Item):
    # define the fields for your item here like:
    # 详情url 
    product_url = scrapy.Field()
    # 性别 男童 女童 baby 
    product_gender = scrapy.Field()

