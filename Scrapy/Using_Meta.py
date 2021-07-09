# -*- coding: utf-8 -*-
"""
Created on Fri Dec  6 15:04:15 2019

@author: anirudh.rao
"""
#import statements
import scrapy
#from pymongo import MongoClient
import unicodedata
import json
import pandas as pd
#client = MongoClient('localhost', 27017)
#db = client.project_49_no
#destCollection = db.nbas_sg

class nbas_sg(scrapy.Spider):
    name = 'bracal'
    def start_requests(self):
        
        url="http://www.brazilcalifornia.com/directory" #main page is parsed
        yield scrapy.Request(url, callback=self.parse, dont_filter=True)
    def parse(self, response):
        rows=response.xpath("//div[@class='col-lg-4 col-md-4 col-sm-4 col-xs-12']/ul/li")
        for row in rows:
            urls=row.xpath(".//a/@href").extract()[0] #getting the category links and parsing them
            urls='http://www.brazilcalifornia.com'+urls
            category=row.xpath(".//a/@title").extract()[0] #getting category and parsing it in meta
#            print(urls)
#            print(category)
            yield scrapy.Request(urls, callback=self.parse_another, dont_filter=True,meta={"category":category})
    def parse_another(self, response):  
        rows1=response.xpath("//div[@class='single-item fi-clear']")
        print(rows1)
        category=response.meta.get("category")
#        print(category)
        for row1 in rows1:
            comp_lin=row1.xpath(".//a/@href").extract()[0] #getting respective company links
#            print(comp_lin)
            yield scrapy.Request(comp_lin, callback=self.parse_anotherr, dont_filter=True,meta={"category":category})
    
    def parse_anotherr(self, response): #writing xpaths to extract the required details
        category=response.meta.get("category")
#        print(category)
        try:
            name=response.xpath("//h2[@class='title-bar']/text()").extract()[0]
        except:
            name=''
#        print(name) 
        try:
            address=response.xpath("//div[@class='col-lg-12 col-md-12 col-sm-12 col-xs-12']/ul/li/strong[contains(text(),'Address')]/parent::li/text() |//div[@class='col-lg-9 col-md-9 col-sm-9 col-xs-8']/ul/li/strong[contains(text(),'Address')]/parent::li/text()").extract()[0].strip().replace("\r"," ").replace("\n"," ").replace("(","").strip()
        except:
            address=''
#        address=address.replace('\r','').replace('\n','').replace('(','').replace(')','')    
#        print(address) 
        try:
            phone=response.xpath("//div[@class='col-lg-12 col-md-12 col-sm-12 col-xs-12']/ul/li/strong[contains(text(),'Phone')]/parent::li/text() |//div[@class='col-lg-9 col-md-9 col-sm-9 col-xs-8']/ul/li/strong[contains(text(),'Phone')]/parent::li/text()").extract()[0].strip()
        except:
            phone=''
#        print(phone)
        try:
            web=response.xpath("//div[@class='col-lg-12 col-md-12 col-sm-12 col-xs-12']/ul/li/strong[contains(text(),'Website')]/parent::li/a/@href |//div[@class='col-lg-9 col-md-9 col-sm-9 col-xs-8']/ul/li/strong[contains(text(),'Website')]/parent::li/a/@href").extract()[0].strip()
        except:
            web=''
#        print(web)
        #store results in a dictionary
        resultDict = {"chamber_name" : "Brazil-California Chamber of Commerce",
                "country" : "USA",
                "region" : 'America',
                "base_url" : "http://www.brazilcalifornia.com",
                "source_url" : response.url,
                "company_website" : web,
                "company_contact" : phone,
                "company_name" : name,
                "company_address" : address,
                  "company_category":category
               
                   }
        print(resultDict)
#        df = pd.DataFrame([resultDict]) #dictionary to dataframe
#        df.to_csv('brazil_california_final1.csv', mode='a', header=False) #writing data frame to csv
