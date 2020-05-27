import scrapy
import re
from scrapy.shell import inspect_response
from scrapy.exceptions import DropItem

#info class is a defult for scrapy items
#see scrapy documentation for more
class Info(scrapy.Item):
    Street = scrapy.Field()
    Postcode = scrapy.Field()
    Vraagprijs = scrapy.Field()
    Aangebodensinds= scrapy.Field()
    Aanvaarding = scrapy.Field()
    Woonoppervlakte = scrapy.Field()
    Perceeloppervlakte = scrapy.Field()
    Inhoud = scrapy.Field()
    Typewoning = scrapy.Field()
    Soortwoning = scrapy.Field()
    Soortbouw = scrapy.Field()
    Bouwjaar = scrapy.Field()
    Aantalkamers = scrapy.Field()
    Aantalslaapkamers = scrapy.Field()
    Aantalbadkamers = scrapy.Field()
    Aantalwoonlagen = scrapy.Field()
    Voorzieningen = scrapy.Field()
    Ligging = scrapy.Field()
    Balkon = scrapy.Field()
    Tuin = scrapy.Field()
    Isolatie = scrapy.Field()
    Verwarming = scrapy.Field()
    Energielable = scrapy.Field()
    Soortparkeergelegenheid = scrapy.Field()
    Url = scrapy.Field()

class Place(scrapy.Item):
    types = scrapy.Field()
    distance = scrapy.Field()

#remove duplicates in the item list 
#see scrapy filters for more
class DuplicateFillter(object):
    def __init__(self):
        self.ids_seen = set()
    def process_items(self, item, spider):
        if item['url'] in self.ids_seen:
            raise DropItem("Duplicate found!")
        else:
            self.ids_seen.add(item['url'])
            return item
class QuotesSpider(scrapy.Spider):
    name = 'house'
    start_urls = [
        'https://www.pararius.nl/koopwoningen/nederland'
    ]
    def __init__(self):
        self.counter = 1
        self.last_page = None

    def parse(self, response):

        if self.last_page == None:
            #print("SHOULD ENTER HERE ONCE")
            self.last_page = int(response.xpath('//li[@class="pagination__item"]/a/@href')[-1].get().replace("/koopwoningen/nederland/page-", ""))
            print(self.last_page)
        for href in response.xpath("//li[@class='search-list__item search-list__item--listing']/section/h2/a/@href").getall():
            yield response.follow(href, self.parse_info)

        href = "https://www.pararius.nl/koopwoningen/nederland/page-"+ str(self.counter)

        if href and self.counter <= self.last_page:
            print("HREFFFF: ", href)
            self.counter += 1
            yield response.follow(href, self.parse)


    def parse_info(self, response):
        res = response.xpath("//dl[@class='listing-features__list']//text()").getall()
        res = [str.strip() for str in res]
        res = list(filter(None,res))
        res[0::2] = [re.sub(r" |-", "", str) for str in res[0::2]]
        res[1::2] = [re.sub(r"€\xa0| k.k.| m²| m³", "", str) for str in res[1::2]]
        res[1] = res[1].replace(".", "")

        street = response.xpath("//h1[@class='listing-detail-summary__title']/text()").get()
        postcode = response.xpath("//div[@class='listing-detail-summary__location']/text()").get().split()[0]
        info = Info()
        info['Street'] = ''
        info['Postcode'] = ''
        info['Vraagprijs'] = ''
        info['Aangebodensinds'] = ''
        info['Aanvaarding'] = ''
        info['Woonoppervlakte'] = ''
        info['Perceeloppervlakte'] = ''
        info['Inhoud'] = ''
        info['Typewoning'] = ''
        info['Soortwoning'] = ''
        info['Soortbouw'] = ''
        info['Bouwjaar'] = ''
        info['Aantalkamers'] = ''
        info['Aantalslaapkamers'] = ''
        info['Aantalbadkamers'] = ''
        info['Aantalwoonlagen'] = ''
        info['Voorzieningen'] = ''
        info['Ligging'] = ''
        info['Balkon'] = ''
        info['Tuin'] = ''
        info['Isolatie'] = ''
        info['Verwarming'] = ''
        info['Energielable'] = ''
        info['Soortparkeergelegenheid'] = ''

        for dt_name, dd_value in zip(res[0::2], res[1::2]):
            dt_name = dt_name.translate({ord(c): "" for c in "!@#$%^&*()[]{};:,./<>?\|`~-=_+"}).replace("\n","").strip("\t").strip().capitalize()
            if dt_name in info.keys():
                info[dt_name] = dd_value

        info['Street'] = street
        info['Postcode'] = postcode
        info['Url'] = response.url
        yield info

ITEM_PIPELINES = {                                                                                          #remove duplicates
    'UH.pipelines.DuplicateFillter': 300,
}
