# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field() 
    title = scrapy.Field()
    date_time = scrapy.Field()
    author = scrapy.Field()
    content = scrapy.Field()
    image_source = scrapy.Field()
    video_source = scrapy.Field()
    article_url = scrapy.Field()
