# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import mysql.connector

class FundaPipeline(object):
    def process_item(self, item, spider):
        return item
    def __init__(self):
        self.create_connection()
        self.create_table()
    
    def create_connection(self):
        self.conn = mysql.connector.connect(
                    host = '192.168.178.11',
                    user = 'root',
                    passwd = 'thang1998',
                    database = 'scraping_data')
        self.cursor = self.conn.cursor()
        
    def create_table(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS funda(
                            Id INT AUTO_INCREMENT,
                            Aangebodensinds TEXT,
                            Status TEXT,
                            Aanvaarding TEXT, 
                            Soortwoonhuis  TEXT,
                            Soortbouw TEXT,
                            Bouwjaar TEXT,
                            Soortdak TEXT,
                            Wonen INT,
                            Overigeinpandigeruimte TEXT,
                            Gebouwgebondenbuitenruimte TEXT,
                            Perceel TEXT, 
                            Inhoud TEXT,
                            Aantalkamers TEXT, 
                            Aantalbadkamers TEXT,
                            Badkamervoorzieningen TEXT,
                            Aantalwoonlagen TEXT,
                            Voorzieningen TEXT,
                            Energielabel TEXT,
                            Isolatie TEXT,
                            Verwarming TEXT,
                            Warmwater TEXT,
                            Cvketel TEXT,
                            Oppervlakte TEXT,
                            Eigendomssituatie TEXT, 
                            Ligging TEXT,
                            Tuin TEXT,
                            Soortgarage TEXT, 
                            Capaciteit TEXT,
                            Soortparkeergelegenheid TEXT, 
                            Adres TEXT, 
                            Postcode INT,
                            Stad TEXT,
                            Prijs INT,
                            Omschrijving TEXT,
                            Aanbieder TEXT,
                            Aanbiederbereikbaar TEXT,
                            Aanbiedertelefoonnummer TEXT,
                            Achtertuin TEXT,
                            Balkondakterras TEXT,
                            Url TEXT,
                            Sold TEXT,
                Verkoopdatum TEXT,
                            Looptijd TEXT,
                            PRIMARY KEY(Id));""")
    def process_item(self, item, spider):
        self.store_db(item)
        return item
    
    def store_db(self, item):

        query = "INSERT INTO funda("
        for i in item.keys():
            query = query + i.strip("'") + ","
        query = query[0:-1] + ") values(" 
        for i in item.keys():
            if item[i] != None:
                item[i] = str(item[i])
                query = query + "'" + item[i].strip().replace("\n", "").replace("\t", "").replace("'",'"').strip() + "'" + ","
            else:
                query = query + "'',"
        query = query[0:-1] + ");"
        self.cursor.execute(query)
        self.conn.commit()
        
   
        
