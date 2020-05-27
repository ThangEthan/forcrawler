import scrapy
import re
from scrapy.shell import inspect_response
from scrapy.exceptions import DropItem

#info class is a defult for scrapy items
#see scrapy documentation for more
class Info(scrapy.Item):
    Neighbourhood = scrapy.Field()
    Street = scrapy.Field()
    Rentpermonth = scrapy.Field()
    Numberofbedrooms = scrapy.Field()
    Postalcode = scrapy.Field()
    Squaremeters = scrapy.Field()
    Availablefrom = scrapy.Field()
    Offeredsince = scrapy.Field()
    energy = scrapy.Field()
    src = scrapy.Field()
    url = scrapy.Field()
    City = scrapy.Field()
    Description = scrapy.Field()
    SellerName = scrapy.Field()
    SellerAddress = scrapy.Field()
    SellerUrl = scrapy.Field()
    SellerPhone = scrapy.Field()
    SellerWebsite = scrapy.Field()
    Active = scrapy.Field()
    
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

#the scrapy spider 
#automaticly running the parse function to loop through the urls
#from the parse func we call the parse_info to actually scrapy and preprocess data
class QuotesSpider(scrapy.Spider):
    name = 'house'
    start_urls = [
        'https://www.pararius.com/apartments'
    ]
    def __init__(self):
        self.counter = 1
        self.last_page = None

    def parse(self, response):
        
        if self.last_page == None:
            #print("SHOULD ENTER HERE ONCE")
            self.last_page = int(response.xpath('//li[@class="last"]/a/@href').get().replace("/apartments/nederland/page-", "")) 
            print(self.last_page)
        for href in response.css('div.details h2 a::attr(href)'):                                           #follow link
            yield response.follow(href, self.parse_info)
        
        href = "https://www.pararius.com/apartments/nederland/page-"+ str(self.counter)
        
        if href and self.counter <= self.last_page: 
            print("HREFFFF: ", href)
            self.counter += 1                         
            yield response.follow(href, self.parse)
    

    def parse_info(self, response):
        details = response.css('div.details-container dd::text').getall()                                   #get address and detail
        details = [str.strip() for str in details]
        
        category = response.xpath("//div[@class='details-container']/dl/dt/text()").getall()
        category = [re.sub(r" ", "", str) for str in category]

        energy = response.xpath("//a[contains(@class, 'popup-link energy-label ')]/text()").get()
        
        inex = response.xpath("//p[@class='price ']/span[@class='inclusive']/text()").get()
        inex = inex.split()                                                                                 #inclusive or exclusive, process string

        disc = response.xpath("//p[@class='text']").get()
        disc = re.sub(r"<(|\/)([a-z][a-z0-9]*)\b[^>]*>|\\t", "", disc)                                      #discription, remove html tag, tab
        
        src = response.css("iframe::attr(src)").get()                                                       #get src for splash.py use on, use for query later
        
        #if we don't define the keys here again the spiders database pipeline will crach given it loops trough the kees **note: we can not retrieve the names of the scrapy.Field objects 
        info = Info()        
        info['Neighbourhood'] = '';  
        info['Street'] = '';
        info['Rentpermonth'] = '';
        info['Numberofbedrooms'] = '';     
        info['Postalcode'] = '';
        info['Squaremeters'] = '';
        info['Availablefrom'] = '';  
        info['Offeredsince'] = '';
        info['City'] = response.xpath("//li[@class='city']/a/span/text()").get()

        #rental agency url on prarius
        info['SellerUrl'] = response.xpath("//p[@class='info']/a/@href").getall()[0]

        #company address needs to be cleaned of \n and \t
        info['SellerAddress'] = response.xpath("//p[@class='info']/text()").getall()[3].replace("\n", "").replace("\t", "")

        #company name
        info['SellerName'] = response.xpath("//p[@class='info']/a/text()").getall()[0]

        #company telephone
        info['SellerPhone'] = response.xpath("//a[@class='cta telephone']/@data-telephone").get()

        #company website
        info['SellerWebsite'] = response.xpath("//a[@class='cta website']/@href").get()
        
        info['Active'] = 1 

        for c, d in zip(category, details):
            c=c.replace(" ", "").replace("\t","").replace("\n","")
            if c in info.keys():
                if c == 'Postalcode' and len(d) > 5:
                    d = d[0:4]
                if c == 'Rentpermonth' or c == 'Squaremeters': 
                    d=d.replace(',', '').replace('€', '')
                if c == 'Squaremeters':
                     d = d.replace(' m²' ,'')
                if d == 'Price on request':
                     d = '-1'
                info[c] = d
        info['energy'] = energy
        info['src'] = src
        info['url'] = response.url
        info['Description'] = disc
        #inspect_response(response, self)
        yield info

ITEM_PIPELINES = {                                                                                          #remove duplicates
    'UH.pipelines.DuplicateFillter': 300,
    
}
