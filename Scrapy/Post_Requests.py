# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 16:06:57 2019

@author: lakshmi.priya
"""
#import statements
import scrapy
from scrapy.http import FormRequest
import xml.etree.ElementTree as ET
import pandas as pd
from unidecode import unidecode
import time

class gastrotage(scrapy.Spider):
   name = 'gastrotage'
   allowed_domains = ['http://www.gastrotage-west.de/']
   def start_requests(self):
#       for i in range(3000,10000):
           frmdata={'domain': '2018_gastrotagewest',
                'topic': '2018_gastrotagewest',
                'appUrl': 'http://www.gastrotage-west.de/ausstellersuche.html?L=1',
                'lang': 'de',
                'apiVersion': '21',
                'useMemcache': 'true',
                'companyid': '5160'}
           url = "https://live.messebackend.aws.corussoft.de/webservice/companydetails"
           yield FormRequest(url, callback=self.parse_another, formdata=frmdata)
           
   def parse_another(self, response):
       time.sleep(10)
       string=response.body
       root = ET.fromstring(string) # gives the root of the xml file
       for child in root: #gives the immediate child tag of the root
           attrib_list = child.attrib # gives the dictionary of attributes inside the child tag
           
           #company name
           try:
               company_name = attrib_list['name']
           except:
               company_name = None
               
#           company_name = unidecode(company_name.encode().decode('utf-8'))
           
           #email
           try:            
               email = attrib_list['email']
           except:
               email =None
           
           #website
           try:
               company_website = attrib_list['web']
           except:
               company_website = None

           #address
           try:
               address1 = attrib_list['adress1']
           except:
               address1 = None

           try:
               postCode = attrib_list['postCode']
           except: 
               postCode = None

           try:
               city = attrib_list['city']
           except:
               city = None

           try:
               country = attrib_list['country']
           except:
               country = None

           try:           
               company_address = address1+','+postCode+' '+city+','+country
           except:
               company_address = None

#           company_address = unidecode(company_address.encode().decode('utf-8')) # to translate the special characters
           
           #phone
           try:
               phone = attrib_list['phone']
               phone = phone.strip('+')
               phone = "Tel:" + phone
           except:   
               phone = None

           #fax
           try:
               fax = attrib_list['fax']
               fax = fax.strip('+')
               fax = "fax:" + fax
           except:
               fax = None

           #result
           if (company_name != None  and company_name != ""):
               resultDict = {
                       "company_website" : company_website,
                       "company_name" : company_name,
                       "company_address" : company_address,
                       "company_phone" : phone,
                       "email" : email,
                       "company_fax" : fax           
                       }
               print(resultDict)
#               df = pd.DataFrame([resultDict])
#               df.to_csv(r'C:\Users\lakshmi.priya\new_link\new_link\spiders\gastrotage_75L_80L.csv', mode='a', header=False)