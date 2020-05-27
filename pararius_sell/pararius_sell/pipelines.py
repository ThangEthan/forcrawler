# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import mysql.connector

#a pipeline for connecting to database and storing scraped data
class ParariusSellPipeline(object):

    def __init__(self):
        print("IN FUCKING PIPELINE")
        self.create_connection()
        self.create_table()
    
    def create_connection(self):
        self.conn = mysql.connector.connect(
                                   host='192.168.178.11',
                                   user='thang',
                                   passwd='thang1998',
                                   database='scraping_data')
        self.cursor = self.conn.cursor()

    def create_table(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS `scraping_data`.`pararius_sell` (
  `Id` INT NOT NULL AUTO_INCREMENT,
  `Vraagprijs` INT NULL,
  `Street` VARCHAR(45) NULL,
  `Postcode` INT NULL,
  `Url` VARCHAR(500) NULL,
  `Aangebodensinds` VARCHAR(45) NULL,
  `Aanvaarding` VARCHAR(45) NULL,
  `Woonoppervlakte` VARCHAR(45) NULL,
  `Perceeloppervlakte` VARCHAR(45) NULL,
  `Inhoud` VARCHAR(45) NULL,
  `Typewoning` VARCHAR(45) NULL,
  `Soortwoning` VARCHAR(45) NULL,
  `Soortbouw` VARCHAR(45) NULL,
  `Bouwjaar` VARCHAR(45) NULL,
  `Aantalkamers` VARCHAR(45) NULL,
  `Aantalslaapkamers` VARCHAR(45) NULL,
  `Aantalbadkamers` VARCHAR(45) NULL,
  `Aantalwoonlagen` VARCHAR(45) NULL,
  `Voorzieningen` VARCHAR(45) NULL,
  `Ligging` VARCHAR(45) NULL,
  `Balkon` VARCHAR(45) NULL,
  `Tuin` VARCHAR(45) NULL,
  `Isolatie` VARCHAR(45) NULL,
  `Verwarming` VARCHAR(45) NULL,
  `Energielable` VARCHAR(45) NULL,
  `Soortparkeergelegenheid` VARCHAR(45) NULL,
  PRIMARY KEY (`Id`),
  `Active` TINYINT(1) NULL,
  `SoldSince` DATE NULL,
  UNIQUE INDEX `Url_UNIQUE` (`Url` ASC) VISIBLE);""");

        

    def process_item(self, item, spider):
        self.store_database(item)
    
    #the Info item object looks like {"Property_name": "Pararius", "Property_owner":"Owner1" }
    #we store owners in a separate table
    def store_database(self, item):
        query = "INSERT INTO pararius_sell("
        values = ""
        for k in item.keys():
            query += str(k)+ ","
            values += "'" + str(item[k]).replace("'",'"').replace(",", " ").strip("\n").strip("\t").strip() + "',"
        query = query[0:-1] + ") values(" + values[0:-1] + ") on duplicate key update active = 1, soldsince = null;"
        #print(query)
        self.cursor.execute(query)
        self.conn.commit()
        
