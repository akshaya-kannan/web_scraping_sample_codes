# -*- coding: utf-8 -*-
"""
Created on Thu Jul 25 12:39:37 2019

@author: akshaya.kannan
"""
#import statements
import scrapy
#from pymongo import MongoClient
from lxml import html
import unicodedata
import json
#client = MongoClient('localhost', 27017)
#db = client.project_61_eu
#destCollection = db.digitaladvertisingawards

class digitaladvertisingawards(scrapy.Spider):
    name = 'digitaladvertisingawards'
    allowed_domains = ['https://www.digitaladvertisingawards.com']
    #df_final = pd.DataFrame()
    
    def start_requests(self):
        for i in range(2014,2020): # looping through years
            url = 'https://www.digitaladvertisingawards.com/digital-trading-awards/digital-trading-awards-'+str(i)
#            print(url)
            yield scrapy.Request(url, callback=self.parse, dont_filter=True)
    def parse(self, response):
        rows=response.xpath("//*[@id='all']/div/article")
        for row in rows:
            award_name=row.xpath(".//header//h3/text()").extract()[0]
            ids=row.xpath(".//header/a/@ajax-id").extract()[0] # extacting ids
#        print(response.url)
            url="https://www.digitaladvertisingawards.com/get-winning-entries/"+str(ids)
#            print(url)
            yield scrapy.Request(url, callback=self.parse_another, dont_filter=True)
    def parse_another(self, response):
        json_data=json.loads(response.text) # response to json
        content=json_data[1].get("data")
        tree=html.fromstring(content) # Get the Document tree from the response variable
        href=tree.xpath("//div[contains(text(),'Award')]/following-sibling::h4/a/@href")
        if href != []:
            url=href[0]
            hrefs="https://www.digitaladvertisingawards.com"+url #getting the required hrefs
#        print(hrefs)
            yield scrapy.Request(hrefs, callback=self.parse_detail, dont_filter=True)
    def parse_detail(self, response): # writing xpaths to extract the required details
        try:
            award_category=response.xpath("//div[@class='entry-info category']/h4[text()='Category']/following-sibling::div/text()").extract()[0]
        except:
            award_category=None
        try:
            company_name=response.xpath("//div[@class='entry-info agency']/h4[text()='Agency']/following-sibling::div//text()").extract()[0]
        except:
            company_name=None
        try:
            company_website=response.xpath("//div[@class='entry-info links']/h4[text()='Links']/following-sibling::div//a/@href").extract()[0]
        except:
            company_website=None
        try:
            year_detail=response.url
            year=year_detail.split("https://www.digitaladvertisingawards.com/digital-trading-awards-")[1].split("/")[0]
        except:
            year=None
#        print(year)
        if company_name != None and company_name != "" :
            resultDict={"award_name" : "The Drum Digital Advertising awards Europe",
	                          "status" : None,
	                           "award_category" : award_category,
	                           "company_name" : company_name,
	                           "company_category" : None,
	                           "company_website" : company_website,
	                           "year" : year,
	                           "base_url" : response.url}
            print(resultDict)
#            destCollection.insert_one(resultDict, True)


        
