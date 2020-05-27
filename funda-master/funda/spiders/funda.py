import scrapy
import re
import os
class Info(scrapy.Field):
    Id = scrapy.Field()
######UNNECESSARY DEFINING OF FIELDS#############
    Aangebodensinds = scrapy.Field()
    Status = scrapy.Field()
    Aanvaarding = scrapy.Field()
    Soortwoonhuis = scrapy.Field()
    Soortbouw = scrapy.Field()
    Bouwjaar = scrapy.Field()
    Soortdak = scrapy.Field()
    Wonen = scrapy.Field()
    Overigeinpandigeruimte = scrapy.Field()
    Gebouwgebondenbuitenruimte = scrapy.Field()
    Perceel = scrapy.Field()
    Inhoud = scrapy.Field()
    Aantalkamers = scrapy.Field()
    Aantalbadkamers = scrapy.Field()
    Badkamervoorzieningen = scrapy.Field()
    Aantalwoonlagen = scrapy.Field()
    Voorzieningen = scrapy.Field()
    Energielabel = scrapy.Field()
    Isolatie = scrapy.Field()
    Verwarming = scrapy.Field()
    Warmwater = scrapy.Field()
    Cvketel = scrapy.Field()
    Oppervlakte = scrapy.Field()
    Eigendomssituatie = scrapy.Field()
    Ligging = scrapy.Field()
    Tuin = scrapy.Field()
    Soortgarage = scrapy.Field()
    Capaciteit = scrapy.Field()
    Soortparkeergelegenheid = scrapy.Field()
    Adres = scrapy.Field()
    Postcode = scrapy.Field()
    Stad = scrapy.Field()
    Prijs =  scrapy.Field()
    Omschrijving = scrapy.Field()
    Url = scrapy.Field()
    Sold = scrapy.Field()
    Verkoopdatum = scrapy.Field()
    Looptijd = scrapy.Field()
    Slaapkamers = scrapy.Field()
    Toiletten = scrapy.Field()

class Funda(scrapy.Spider):
    name = "funda"
    #start_urls = ['file:///home/vuvietthang/Huis%20te%20koop_%20Naaldakker%207%205094%20HC%20Lage%20Mierde%20[funda].html']
    #added 12/07/2019
    path = "file:///home/crawler1/house/"
    start_urls = []
    for filename in os.listdir("/home/crawler1/house"):
        if filename.endswith(".html"):
            start_urls.append(path + filename)


    def parse(self, response):
        res = response.xpath("//div[@class='object-kenmerken-body']//text()[not(ancestor::h3)][not(ancestor::div[@class='' or @class='kadaster-title'])][not(ancestor::a)]").getall()
        res = [re.sub(r"\r\n","",str) for str in res ]
        res = [str.strip() for str in res]
        res = list(filter(None, res))

        res[0::2] = [re.sub(r" |-", "", str) for str in res[0::2]]
        res[1::2] = [re.sub(r" januari ", "-01-", str) for str in res[1::2]]
        res[1::2] = [re.sub(r" februari ", "-02-", str) for str in res[1::2]]
        res[1::2] = [re.sub(r" maart ", "-03-", str) for str in res[1::2]]
        res[1::2] = [re.sub(r" april ", "-04-", str) for str in res[1::2]]
        res[1::2] = [re.sub(r" mei ", "-05-", str) for str in res[1::2]]
        res[1::2] = [re.sub(r" juni ", "-06-", str) for str in res[1::2]]
        res[1::2] = [re.sub(r" juli ", "-07-", str) for str in res[1::2]]
        res[1::2] = [re.sub(r" augustus ", "-08-", str) for str in res[1::2]]
        res[1::2] = [re.sub(r" september ", "-09-", str) for str in res[1::2]]
        res[1::2] = [re.sub(r" oktober ", "-10-", str) for str in res[1::2]]
        res[1::2] = [re.sub(r" november ", "-11-", str) for str in res[1::2]]
        res[1::2] = [re.sub(r" december ", "-12-", str) for str in res[1::2]]
        info = Info()
        #added 12/07/2019
        info['Url'] = response.xpath("//link[@rel='canonical']/@href").get().replace('verkocht/','')
        info['Sold'] = "False"
        info['Adres'] = response.xpath("//span[@class='object-header__title']//text()").get()
        info['Postcode'] = response.xpath("//span[@class='object-header__subtitle']//text()").get()
        info['Postcode'] = info['Postcode'][0:4] if info['Postcode'] != None else ""
        info['Stad'] = response.xpath("//span[@class='object-header__subtitle']//text()").get()
        info['Stad'] = info['Stad'][7:] if info['Stad'] != None else ""
        try:
            currency, price, utilities = response.xpath("//strong[@class='object-header__price']//text()").get().split(" ")
        except:
            currency, price, utilities = response.xpath("//strong[@class='object-header__price--historic']//text()").extract()[0].split(" ")
            info["Sold"] = "True"


        info['Prijs'] = price.replace('.','')

        #description = response.xpath("//div[@class='object-description-body']/text()").extract()
        #processed_description = ""
        #for item in description:
        #    processed_description += item.replace("\n","").strip()
        #info['Omschrijving'] = processed_description


        info['Aangebodensinds'] = ""
        info['Status'] = ""
        info['Aanvaarding'] = ""
        info['Soortwoonhuis'] = ""
        info['Soortbouw'] = ""
        info['Bouwjaar'] = ""
        info['Soortdak'] = ""
        info['Wonen'] = ""
        info['Overigeinpandigeruimte'] = ""
        info['Gebouwgebondenbuitenruimte'] = ""
        info['Perceel'] = ""
        info['Inhoud'] = ""
        #info['Aantalkamers'] = ""
        #info['Slaapkamers'] = None
        #info['Aantalbadkamers'] = ""
        #info['Toiletten'] = None
        info['Badkamervoorzieningen'] = ""
        info['Aantalwoonlagen'] = ""
        info['Voorzieningen'] = ""
        info['Energielabel'] = ""
        info['Isolatie'] = ""
        info['Verwarming'] = ""
        info['Warmwater'] = ""
        info['Cvketel'] = ""
        info['Oppervlakte'] = ""
        info['Eigendomssituatie'] = ""
        info['Ligging'] = ""
        info['Tuin'] = ""
        info['Soortgarage'] = ""
        info['Capaciteit'] = ""
        info['Soortparkeergelegenheid'] = ""
        info['Verkoopdatum'] = ""
        info['Looptijd'] = ""

        #added 17/07/2019
        #Owner/Retailer contact
        info["Aanbieder"] = response.xpath("//a[@class='object-contact-aanbieder-link']//text()").get()
        info["Aanbiederbereikbaar"] = response.xpath("//span[@class='object-contact-text__content']//text()").get()
        info["Aanbiedertelefoonnummer"] = response.xpath("//div[@class='object-contact-show-phonenumber']/a/@href").get()
        info["Aanbiedertelefoonnummer"] = info["Aanbiedertelefoonnummer"].replace("tel:", "") if info["Aanbiedertelefoonnummer"] != None else ""
        info["Aanbiedertelefoonnummer"] = info["Aanbiedertelefoonnummer"] if info["Aanbiedertelefoonnummer"] != None else ""
        info["Achtertuin"] = ""
        info["Balkondakterras"] = ""
        #done 17/07/2019

        #changed 16/07/2019
        for dt_name, dd_value in zip(res[0::2], res[1::2]):
            dt_name = dt_name.translate({ord(c): "" for c in "!@#$%^&*()[]{};:,./<>?\|`~-=_+"}).replace("\n","").strip("\t").strip().capitalize()
            if dt_name == "Aantalkamers":
                kamer = re.search('([0-9]+) kamers?.(\(([0-9]+) slaapkamers?\))?', dd_value)
                if kamer.group(1) != None: info['Aantalkamers'] = kamer.group(1)  
                if kamer.group(3) != None: info['Slaapkamers'] = kamer.group(3) 
            elif dt_name == "Aantalbadkamers": 
                kamer = re.search('(([0-9]+) badkamers?)?(.*?([0-9]+).*)?', dd_value) 
                if kamer.group(2) != None: info['Aantalbadkamers'] = kamer.group(2)
                if kamer.group(4) != None: info['Toiletten'] = kamer.group(4)
            if dt_name in info.keys():
                if dt_name in {'Inhoud', 'Oppervlakte', 'Perceel', 'Gebouwgebondenbuitenruimte', 'Wonen', 'Overigeinpandigeruimte'}:
                    info[dt_name] = dd_value.replace(".","").replace(" m²","").replace(" m³","")
                elif dt_name in {'Aantalkamers', 'Aantalbadkamers'}:
                    continue
                else:
                    info[dt_name] = dd_value
        yield info
