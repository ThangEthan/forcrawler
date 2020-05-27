# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import mysql.connector
from datetime import date

class ReservedPipeline(object):

    def process_item(self, item, spider):
        self.store_db(item)
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
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS reserved(
                                ID INT AUTO_INCREMENT PRIMARY KEY,                               
                                Url VARCHAR(500) UNIQUE,
                                Status TEXT
                                );""")
    
    def store_db(self, item):
        today = date.today().strftime("%d-%m-%Y")
        for i in range(0, len(item["Url"])):
            if (item["Status"][i] == 'Verkocht onder voorbehoud'):
                query="INSERT IGNORE INTO reserved(Url, Status, VerkochtOnderVoorbehoud, Onderbod) values('" + item["Url"][i] + "', '" + item["Status"][i] + "', '" + today + "', null);"
                self.cursor.execute(query)
            elif (item["Status"][i] == 'Onder bod'):
                query="INSERT IGNORE INTO reserved(Url, Status, VerkochtOnderVoorbehoud, Onderbod) values('" + item["Url"][i] + "', '" + item["Status"][i] + "', null, '" + today + "');"
                self.cursor.execute(query) 
        self.conn.commit()