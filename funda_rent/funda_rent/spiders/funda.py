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
    Rented = scrapy.Field()
    Verhuurdatum = scrapy.Field()
    Looptijd = scrapy.Field()
    Waarborgsom = scrapy.Field()

class Funda(scrapy.Spider):
    name = "funda_rent"
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
        info = Info()
        #added 12/07/2019
        info['Url'] = response.xpath("//link[@rel='canonical']/@href").get().replace('verhuurd/','')
        info['Rented'] = "False"
        info['Adres'] = response.xpath("//span[@class='object-header__title']//text()").get()
        info['Postcode'] = response.xpath("//span[@class='object-header__subtitle']//text()").get()
        info['Postcode'] = info['Postcode'][0:4] if info['Postcode'] != None else ""
        info['Stad'] = response.xpath("//span[@class='object-header__address-city']//text()").get()
        info['Stad'] = info['Stad'][7:] if info['Stad'] != None else ""
        try:
            currency, price, utilities = response.xpath("//strong[@class='object-header__price']//text()").get().split(" ")
        except:
            price = response.xpath("//strong[@class='object-header__price--historic']//text()").get().replace("€ ", "").replace(" /mnd", "")
            info["Rented"] = "True"


        info['Prijs'] = price.replace('.','')

        description = response.xpath("//div[@class='object-description-body']/text()").extract()
        processed_description = ""
        for item in description:
            processed_description += item.replace("\n","").strip()
        info['Omschrijving'] = processed_description


        info['Aangebodensinds'] = ""
        info['Status'] = ""
        info['Aanvaarding'] = ""
        info['Soortwoonhuis'] = ""
        info['Soortbouw'] = ""
        info['Bouwjaar'] = ""
        info['Soortdak'] = ""
        info['Wonen'] = "-1"
        info['Overigeinpandigeruimte'] = ""
        info['Gebouwgebondenbuitenruimte'] = ""
        info['Perceel'] = ""
        info['Inhoud'] = ""
        info['Aantalkamers'] = ""
        info['Aantalbadkamers'] = ""
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
        info['Verhuurdatum'] = ""
        info['Looptijd'] = ""
        info['Waarborgsom'] = "0"

        #added 17/07/2019
        #Owner/Retailer contact
        info["Aanbieder"] = response.xpath("//a[@class='object-contact-aanbieder-link']//text()").get()
        info["Aanbiederbereikbaar"] = response.xpath("//span[@class='object-contact-text__content']//text()").get()
        info["Aanbiedertelefoonnummer"] = response.xpath("//div[@class='object-contact-show-phonenumber']/a/@href").get()
        info["Aanbiedertelefoonnummer"] = info["Aanbiedertelefoonnummer"].replace("tel:", "") if info["Aanbiedertelefoonnummer"] != None else ""
        info["Aanbiedertelefoonnummer"] = info["Aanbiedertelefoonnummer"] if info["Aanbiedertelefoonnummer"] != None else ""
        info["Achtertuin"] = ""
        #done 17/07/2019

        #changed 16/07/2019
        for dt_name, dd_value in zip(res[0::2], res[1::2]):
            dt_name = dt_name.translate({ord(c): "" for c in "!@#$%^&*()[]{};:,./<>?\|`~-=_+"}).replace("\n","").strip("\t").strip().capitalize()
            if dt_name == 'Waarborgsom':
                dd_value = dd_value.replace('€ ','').replace(' eenmalig', '').replace('.','')

            if dt_name == 'Wonen':
                dd_value = dd_value.replace(" m²","")
                

            if dt_name == 'Waarborgsom' and (dd_value == 'Geen' or dd_value == ''):
                dd_value = "0"

            if dt_name in info.keys():
                info[dt_name] = dd_value
        yield info
