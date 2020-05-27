import scrapy
import re
import os
class Info(scrapy.Field):
    Status=scrapy.Field()
    Url=scrapy.Field()

class Reserved(scrapy.Spider):
    name = "reserved"
    path = "file:///home/crawler1/house/"
    start_urls = []
    for filename in os.listdir("/home/crawler1/house"):
        if filename.endswith(".html"):
            start_urls.append(path + filename)
    
   
        
    #start_urls = ["file:///Users/thangvu/funda.html"]
    def parse(self, response):
        info = Info()
        info["Status"]=response.xpath("//ol[@class='search-results']/li[@class='search-result']//li[@class='label label-transactie-voorbehoud']/text()").getall()
        url = response.xpath("//ol[@class='search-results']/li[@class='search-result']//a[@data-object-url-tracking='resultlist'][2]/@href").getall()
        info["Url"] = ["https://www.funda.nl" + str for str in url]
        
        yield info
