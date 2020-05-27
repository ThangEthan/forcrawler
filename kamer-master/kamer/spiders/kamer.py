import scrapy
import re
from scrapy.shell import inspect_response
from scrapy.http import FormRequest
from scrapy.utils.response import open_in_browser
from scrapy.exceptions import DropItem
import json

class Info(scrapy.Item):
    Id = scrapy.Field()
    Woonkamer = scrapy.Field()
    Keuken = scrapy.Field()
    Badkamer =scrapy.Field()
    Toilet= scrapy.Field()
    Internet= scrapy.Field()
    Energielabel= scrapy.Field()
    Huisgenoten= scrapy.Field()
    Geslacht= scrapy.Field()
    Huisdieren= scrapy.Field()
    Binnenroken= scrapy.Field()
    Inex= scrapy.Field()
    Price= scrapy.Field()
    Opleverniveau= scrapy.Field()
    Beschikbaarheid= scrapy.Field()
    Description = scrapy.Field()
    Ownername= scrapy.Field()
    Typeaanbieder= scrapy.Field()
    Actiefsinds= scrapy.Field()
    Laatstgezienop= scrapy.Field()
    Aantalkeerverhuurdviakamernet = scrapy.Field()
    Responserate= scrapy.Field()
    Reactietijd= scrapy.Field()
    Url= scrapy.Field()
    Street= scrapy.Field()
    City= scrapy.Field()
    Surface=scrapy.Field()
    SellerUrl=scrapy.Field()
    Type = scrapy.Field()
    Active = scrapy.Field()

class Kamer(scrapy.Spider):
    name = 'kamer'
    start_urls = ['https://kamernet.nl/performlogin']

    def parse(self, response):
        formdataa = {
            "UserEmail": 'meohen98@yahoo.com.vn',
            "LoginPassword": 'thang1998',
            "LoginReturnUrl": 'https://kamernet.nl/huren/kamers-nederland',
            "RememberMe": 'TRUE',
            "JavascriptCallback": "",
            "Source": ""

        }
        return FormRequest.from_response(response, formdata = formdataa, callback = self.parse_ad)

    def parse_ad(self, response):
        #f = open('l1.txt', 'r')
        #for href in f:
        #    yield response.follow(href.strip(), self.parse_info)

        for href in response.xpath("//div[@class='tile-img']/a"):
            yield response.follow(href, self.parse_info) #(url to follow, callback,...)

        pageno = response.xpath("//li[@class='next waves-effect']/@page").get()

        if pageno:
            yield response.follow("https://kamernet.nl/huren/kamers-nederland"+'?pageno='+str(pageno), self.parse_ad)

    def parse_info(self, response): #the scraping
        #open_in_browser(response)
        res = response.xpath("//div[@class='left']/*/text()").getall()
        res = [re.sub(r" |\r\n","",str) for str in res ]
        price = response.xpath("//div[@class='price left']/text()").get()
        price = re.sub(r" ", "", price)
        inex = response.xpath("//div[@class='gwe']/text()").get()
        des = response.xpath("//div[@class='col s12 room-description desc-special-text']").get()
        des = re.sub(r"<(|\/)([a-z][a-z0-9]*)\b[^>]*>|\\t", "", des)
        info = Info()

        owner = response.xpath("//div[@class='hide-on-small-only']/table/tbody/tr/*/text()").getall()
        owner[0::2] = [re.sub(r" |:", "", str) for str in owner[0::2]]

        street = response.xpath("//span[@class='h1_line2']/text()").get()
        city = response.xpath("//span[@class='h1_line3']/text()").get()[3:]

        info['Woonkamer'] = ""
        info['Keuken'] = ""
        info['Badkamer'] = ""
        info['Toilet'] = ""
        info['Internet'] = ""
        info['Energielabel'] = ""
        info['Huisgenoten'] = ""
        info['Geslacht'] = ""
        info['Huisdieren'] = ""
        info['Binnenroken'] = ""
        info['Inex'] = ""
        info['Price'] = ""
        info['Opleverniveau'] = ""
        info['Beschikbaarheid'] = ""
        info['Description'] = ""
        info['Ownername'] = ""
        info['Typeaanbieder'] = ""
        info['Actiefsinds'] = ""
        info['Laatstgezienop'] = ""
        info['Aantalkeerverhuurdviakamernet'] = "0"
        info['Responserate'] = ""
        info['Reactietijd'] = ""
        info['Url'] = ""
        info['Street'] = ""
        info['City'] = ""
        info['Surface'] = "-1"
        info['SellerUrl'] = ""
        info['Active'] = 1
        for column_name, column_value in zip(res[0::2], res[1::2]):
            column_name = column_name.translate({ord(c): "" for c in "!@#$%^&*()[]{};:,./<>?\|`~-=_+'"}).replace("\n","").replace("\t", "").replace(" ", "").strip().capitalize()
            if column_name in info.keys():
                info[column_name] = column_value.replace("\n", "").replace("\t", "")

        for column_name, column_value in zip(owner[0::2], owner[1::2]):
            column_name = column_name.translate({ord(c): "" for c in "!@#$%^&*()[]{};:,./<>?\|`~-=_+'"}).capitalize().replace("\n","").replace("\t", "").replace(" ", "").strip()
            if column_name in info.keys():
                info[column_name] = column_value.replace("\n", "").replace("\t", "")


        info['Price'] = price.replace("\n","").replace("\t", "").replace("€", "").strip()
        info['Inex'] = inex.replace("\n","").replace("\t", "").strip()
        info['Opleverniveau'] = response.xpath("//div[@class='furnishing']/text()").get().replace("\n","").replace("\t", "").strip()
        info['Beschikbaarheid'] = response.xpath("//div[@class='availability']/text()").get().replace("\n","").replace("\t", "").strip()
        info['Description'] = des.replace("\n","").replace("\t", "").strip()
        info['Url'] = response.url.replace("\n","").replace("\t", "").strip()
        info['Type'] = response.xpath("//span[@class='h1_line1']/text()").get().split(' ')[0]
        info['Street'] = street.replace("\n","").replace("\t", "").strip()
        info['City'] = city.replace("\n","").replace("\t", "").strip()
        info['Surface'] = response.xpath("//div[@class='surface left']/text()").get().replace(' m','')
        info['Ownername'] = response.xpath("//div[@class='owner-name']/text()").get()
        info['SellerUrl'] = response.xpath("//div[@id='user-image-link']/@onclick").get().replace("')","").replace("'","").replace("javascript:NavigateToLandlord(","")
        info['SellerUrl'] = re.sub(r'/displayroomadvert.*', '', info['SellerUrl'])
        yield info

#ITEM_PIPELINES = {'kamer.pipelines.DuplicateFillter': 300,}
