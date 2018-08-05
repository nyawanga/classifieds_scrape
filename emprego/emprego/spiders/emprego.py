from bs4 import BeautifulSoup as bs
import html5lib
import re
from datetime import datetime as dt
import json

import scrapy
from scrapy.selector import Selector
from emprego.items import EmpregoItem

class EmpregoJobs(scrapy.Spider):
    name = 'emprego'
    items = EmpregoItem()

    #start_urls = ['https://en.emprego.mmo.co.mz/jobs/page/2/']

    def start_requests(self):
        urls = ['https://en.emprego.mmo.co.mz']
        urls.extend(['https://en.emprego.mmo.co.mz/jobs/page/{0}/'.format(i) for i in range(100)])
        for url in urls:
        	yield scrapy.Request(url = url, callback = self.parse)


    def parse(self, response):
        #jobs_table = response.selector.xpath('//li[@class= "job" or @class= "job job-alt"]//div[@class = "job-title"]//h3/a/@href')
        #jobs_table = response.selector.xpath('//div[@class="job-title"]')
   #     job_pages = [div.xpath('./h3/a/@href').extract_first().strip() for div in jobs_table]
    	#page = response.url.split("/")
        # if jobs_table:
        #     count = 0
        main_xpath = '//li[@class= "job" or @class= "job job-alt"]//div[@class = "job-title"]//h3/a/@href'
        for page in response.selector.xpath(main_xpath).extract()[0:2]:
            yield  scrapy.Request( response.urljoin(page), callback = self.parse_details )

        
        #next_page = response.selector.xpath('//div[@class= "paging"]//a[@class= "next page-numbers"]/@href').extract()
        # next_page_xpath = '//div[@class= "paging"]//a[@class= "next page-numbers"]/@href'
        # for page in response.selector.xpath(next_page_xpath).extract():
        #     yield scrapy.Request(response.urljoin(page), callback = self.parse)

    	# filename = 'response.html'
    	# with open(filename, 'wb') as f:
    	# 	f.write(response.body)
    	# self.log('Saved file {}'.format(filename))

    def parse_details(self, response):
        job_page = response.selector.xpath('//div[@class= "section single"]')
        #jobs_meta = response.selector.xpath('//div[starts-with(@class, "job-meta")]') 
        jobs_meta = job_page.xpath('//div[starts-with(@class, "job-meta")]')
        title = job_page.xpath('div/h1[@class= "title"]/text()').extract_first().strip()
        jobtype = jobs_meta.xpath('span[@class = "job-type"]/span/text()').extract_first()
        location = jobs_meta.xpath('span[@class = "location"]/span/text()').extract_first()
        organisation = jobs_meta.xpath('span[@class = "company"]/text()').extract_first()
        date_posted = jobs_meta.xpath('span[@class = "date"]/text()').extract_first()
        footer_div = job_page.xpath('//div[@class= "content-bar iconfix foot"]')
        category = footer_div.xpath('p[@class= "meta"]//a/text()').extract_first()
        days_to_expiry = footer_div.xpath('p[@class= "meta"]//span[@class= "expiry"]/text()').extract_first()
        contents_table = bs(response.body, 'html.parser').find('div', {'class': 'section_content'}).children
        job_details = self.process_details_soup(contents_table)

        if job_page:
            self.items['url'] = response.url
            self.items['title'] = title
            self.items['jobtype'] = jobtype
            self.items['location'] = location
            self.items['organisation'] = organisation
            self.items['date_posted'] = date_posted
            self.items['category'] = category
            self.items['days_to_expiry'] = days_to_expiry
            self.items['job_details'] = job_details
            yield self.items
        else:
            pass

        


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

    def errback_httpbin(self, failure):
        if failure.check(HttpError):
            response = failure.value.response
            self.logger.error('HttpError on %s', response.url)

        elif failure.check(DNSLookupError):
            # this is the original request
            request = failure.request
            self.logger.error('DNSLookupError on %', request.url)

        elif failure.check(TimoutError, TCPTimedOutError):
            request = failure.request
            self.logger.error('TImeoutError on %s', request.url)

        else:
            #log all failures if it is none of the above
            self.logger.error(repr(failure))

