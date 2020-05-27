# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import mysql.connector


class UhPipeline(object):
    def __init__(self):
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
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS pararius(
                                                        Id INT AUTO_INCREMENT PRIMARY KEY,
                                                        Neighbourhood TEXT,
                                                        Street TEXT,
                                                        Rentpermonth INT,
                                                        Numberofbedrooms TEXT,
                                                        Postalcode INT,
                                                        Squaremeters INT,
                                                        Availablefrom TEXT,
                                                        Offeredsince TEXT,
                                                        energy TEXT,
                                                        src TEXT,
                                                        url TEXT,
                                                        City TEXT,
                                                        Description TEXT,
                                                        SellerUrl TEXT);""");
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS pararius_owner(
                                                        Id INT AUTO_INCREMENT PRIMARY KEY,
                                                        SellerName TEXT,
                                                        SellerAddress TEXT,
                                                        SellerUrl TEXT,
                                                        SellerPhone TEXT,
                                                        SellerWebsite TEXT
                                                        );""");

        

    def process_item(self, item, spider):
        self.store_database(item)

    #the Info item object looks like {"Property_name": "Pararius", "Property_owner":"Owner1" }
    #we store owners in a separate table
    def store_database(self, item):
        query = "INSERT INTO pararius("
        owner_query = "INSERT IGNORE INTO pararius_owner("
        values = ""
        owner_values = ""
        for k in item.keys():
            if item[k] == None:
                item[k] = ''
                if k in ['Rentpermonth', 'Squaremeters', 'Postalcode']:
                    item[k] = '-1'
            if "Seller" in k:
                owner_query += str(k)+ ","
                owner_values += "'" + str(item[k]).replace("'",'"').replace(",", " ").strip("\n").strip("\t").strip() + "',"
                if "SellerUrl" != k:
                    continue
            query += str(k)+ ","
            values += "'" + str(item[k]).replace("'",'"').replace(",", " ").strip("\n").strip("\t").strip() + "',"
        query = query[0:-1] + ") values(" + values[0:-1] + ") on duplicate key update active = 1, RentedSince = null;"
        owner_query = owner_query[0:-1] + ") values(" + owner_values[0:-1] + ");"

        self.cursor.execute(query)
        self.cursor.execute(owner_query)
        self.conn.commit()
        
