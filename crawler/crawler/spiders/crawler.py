#https://medium.com/python-pandemonium/develop-your-first-web-crawler-in-python-scrapy-6b2ee4baf954
#http://rlanders.net/scrapy/

from bs4 import BeautifulSoup as bs
import html5lib
import re
from datetime import datetime as dt
import json

import scrapy
from crawler.items import CrawlerItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from lxml import html

class CrawlerSpider(CrawlSpider):
    name = "crawler"
    #allowed_domains = 'emprego.co.mz'

    next_page_xpath = '//div[@class= "paging"]//a[@class= "next page-numbers"]'
    start_urls = (
        'https://en.emprego.mmo.co.mz',
        'https://en.emprego.mmo.co.mz/jobs/page/2/',
        )
    rules = (
        Rule(LinkExtractor(allow =(), restrict_xpaths = [next_page_xpath,] #restrict_css = (".page-numbers", ) 
                          ), callback = 'parse_next_page', follow = True
           ),)

    def parse_next_page(self, response):
        main_xpath = '//li[@class= "job" or @class= "job job-alt"]//div[@class = "job-title"]//h3/a/@href'
        job_pages = response.selector.xpath(main_xpath).extract()[0:2]
        for page in job_pages:
            yield scrapy.Request(page, callback = self.parse_details)
            #print('Processing.. :' + response.url)

    def parse_details(self, response):
        items = CrawlerItem()
        # items = CrawlerItem()
        job_page = response.selector.xpath('//div[@class= "section single"]')
        #jobs_meta = response.selector.xpath('//div[starts-with(@class, "job-meta")]') 
        jobs_meta = job_page.xpath('//div[starts-with(@class, "job-meta")]')
        items['url'] = response.url  
        items['title'] = job_page.xpath('div/h1[@class= "title"]/text()').extract_first().strip()
        items['jobtype'] = jobs_meta.xpath('span[@class = "job-type"]/span/text()').extract_first()
        items['location'] = jobs_meta.xpath('span[@class = "location"]/span/text()').extract_first()
        items['organisation'] = jobs_meta.xpath('span[@class = "company"]/text()').extract_first()
        items['date_posted'] = jobs_meta.xpath('span[@class = "date"]/text()').extract_first()
        footer_div = job_page.xpath('//div[@class= "content-bar iconfix foot"]')
        items['category'] = footer_div.xpath('p[@class= "meta"]//a/text()').extract_first()
        items['days_to_expiry'] = footer_div.xpath('p[@class= "meta"]//span[@class= "expiry"]/text()').extract_first()
        contents_table = bs(response.body, 'html.parser').find('div', {'class': 'section_content'}).children
        items['job_details'] = self.process_details_soup(contents_table)
        #items['job_details'] = html.fromstring(job_page.xpath('//div[@class= "section_content"]').extract()).text_content().strip()

        yield items

    def process_details_soup(self, contents_table):
        content_string = []
        for child in contents_table : #.get_text(strip = True)#.strip()
            if child.name == 'center':
                continue
            elif child.name == 'div' and child.find('div', {'class':'wpa'}): 
                #print("Found it %s" % "".join(child.get('class')) )
                break                                 # Break after getting to end of details
            elif child.string == None:
                #print(child.get_text("\n", strip = True)) 
                content_string.append(child.get_text("\n", strip = True))    # Mainly for items in a list
            else:
                #print(child.string, "\n")
                content_string.append(child.string.strip())           #Get none list content
        return "\n".join(content_string)

