# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    url = scrapy.Field()
    title = scrapy.Field()
    organisation = scrapy.Field()
    location = scrapy.Field()
    jobtype = scrapy.Field()
    job_details = scrapy.Field()
    category = scrapy.Field()
    date_posted = scrapy.Field()
    days_to_expiry = scrapy.Field()
#    pass
