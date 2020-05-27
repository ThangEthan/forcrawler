
import scrapy
import re
import os


class Info(scrapy.Field):
    Id = scrapy.Field()
######UNNECESSARY DEFINING OF FIELDS#############
    Aangebodensinds = scrapy.Field()
    Status = scrapy.Field()
    Verhuurdatum = scrapy.Field()
    Looptijd = scrapy.Field()
    Url = scrapy.Field()


class Funda(scrapy.Spider):
    name = "funda_rented"
    path = "file:///home/crawler1/house/"
    start_urls = []
    for filename in os.listdir("/home/crawler1/house"):
        if filename.endswith(".html"):
            start_urls.append(path + filename)

    def parse(self, response):
        res = response.xpath(
            "//div[@class='object-kenmerken-body']//text()[not(ancestor::h3)][not(ancestor::div[@class='' or @class='kadaster-title'])][not(ancestor::a)]").getall()
        res = [re.sub(r"\r\n", "", str) for str in res]
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
        # added 12/07/2019
        info['Aangebodensinds'] = ""
        info['Status'] = ""
        info['Verhuurdatum'] = ""
        info['Looptijd'] = ""
        info['Rented'] = "True"
        info['Url'] = response.xpath("//link[@rel='canonical']/@href").get().replace('verhuurd/','') 
        for dt_name, dd_value in zip(res[0::2], res[1::2]):
            dt_name = dt_name.translate(
                {ord(c): "" for c in "!@#$%^&*()[]{};:,./<>?\|`~-=_+"}).replace("\n", "").strip("\t").strip().capitalize()
            if dt_name in info.keys():
                info[dt_name] = dd_value.replace(" m²", "")

        yield info
