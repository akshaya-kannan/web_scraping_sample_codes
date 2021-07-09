# -*- coding: utf-8 -*-
"""
Created on Fri Dec  6 15:04:15 2019

@author: akshaya.kannan
"""
#import statements
import scrapy
from pymongo import MongoClient
import unicodedata
import json
import pandas as pd

class nbas_sg(scrapy.Spider):
    name = 'nbcc'
    allowed_domains = ["nbcc.com.br"]
    def start_requests(self):
        
        url="https://nbcc.com.br/nbcc-members/" # main page is parsed
        yield scrapy.Request(url, callback=self.parse, dont_filter=True)
    def parse(self, response):
        rows=response.xpath("//ul[@class='members-listing']/li")
        for row in rows:
            urls=row.xpath(".//a/@href").extract()[0] # getting member links
            
            print(urls)
            
            yield scrapy.Request(urls, callback=self.parse_anotherr, dont_filter=True)
#   
    def parse_anotherr(self, response): 
       
        try:
            name=response.xpath("//h1[@class='post entry-title']/text()").extract()[0]
        except:
            name=''
#        print(name) 
        try:
            cat=response.xpath("//strong[contains(text(),'Category')]/parent::li/ul/li/text()").extract()[0].strip() #use of contains and parent
        except:
            cat=''
#        print(cat) 
        try:
            phone=','.join(response.xpath("//strong[contains(text(),'Phone')]/parent::li/text()").extract())
        except:
            phone=''
        print(phone)
        try:
            web=response.xpath("//strong[contains(text(),'Site')]/parent::li/a/@href").extract()[0].strip()
        except:
            web=''
#        print(web)
        #store results in a dictionary
        resultDict = {"chamber_name" : "Norwegian Brazillian Chamber of Commerce",
                "country" : "Norway",
                "region" : 'Europe',
                "base_url" : "https://nbcc.com.br",
                "source_url" : response.url,
                "company_website" : web,
                "company_contact" : phone,
                "company_name" : name,
                "company_address" : None,
                  "company_category":cat
               
                   }
        print(resultDict)
        df = pd.DataFrame([resultDict])  #dictionary to dataframe
        df.to_csv('nbcc.csv', mode='a', header=False) #writing data frame to csv
