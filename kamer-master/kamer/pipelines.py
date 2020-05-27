# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import mysql.connector

class KamerPipeline(object):

    def __init__(self):
        self.create_connection()
        self.create_table()

    def create_connection(self):
        self.conn = mysql.connector.connect(
                                        host = '192.168.178.11',
                                        user = 'thang',
                                        passwd = 'thang1998',
                                        database = 'scraping_data')
        self.cursor = self.conn.cursor()

    def create_table(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS kamer(
                            Id INT AUTO_INCREMENT PRIMARY KEY,
                            Woonkamer TEXT,
                            Keuken TEXT,
                            Badkamer TEXT,
                            Toilet TEXT,
                            Internet TEXT,
                            Energielabel TEXT,
                            Huisgenoten TEXT,
                            Geslacht TEXT,
                            Huisdieren TEXT,
                            Binnenroken TEXT,
                            Inex TEXT,
                            Price TEXT,
                            Opleverniveau TEXT,
                            Beschikbaarheid TEXT,
                            Description TEXT,
                            Ownername TEXT,
                            Typeaanbieder TEXT,
                            Actiefsinds TEXT,
                            Laatstgezienop TEXT,
                            Aantalkeerverhuurdviakamernet TEXT,
                            Responserate TEXT,
                            Reactietijd TEXT,
                            Url TEXT,
                            Street TEXT,
                            City TEXT,
                            Surface TEXT,
                            SellerUrl TEXT,
                            SellerPhone TEXT);""")

    def process_item(self, item, spider):
        self.store_database(item)
    def store_database(self,item):
        query = "INSERT INTO kamer("
        owner_query = "INSERT INTO kamer_owner("
        values = ""
        owner_value = ""
        owner_update = ""
        for k in item.keys():
            if k in ["Aantalkeerverhuurdviakamernet","Ownername","Typeaanbieder","Actiefsinds","Laatstgezienop", "Responserate","Reactietijd", "SellerUrl"]:
                owner_query += str(k)+ ","
                owner_value += "'" + str(item[k]).replace("'",'"').replace(",", ";").strip("\n").strip("\t").strip() + "',"
                if k != "SellerUrl":
                    owner_update += str(k) + "='" + str(item[k]) + "', "
                    continue

            query += str(k)+ ","
            values += "'" + str(item[k]).replace("'",'"').replace(",", ";").strip("\n").strip("\t").strip() + "',"

        query = query[0:-1] + ") values(" + values[0:-1] + ") on duplicate key update active = 1, rentedsince = null;"
        owner_query = owner_query[0:-1] + ") values(" + owner_value[0:-1] + ") on duplicate key update "
        owner_query += owner_update[0:-2] +";"
        #print(query)
        self.cursor.execute(query)
        self.cursor.execute(owner_query)
        self.conn.commit()

    def update_database(self, item):
        query = "UPDATE kamer SET surface=" + "'" + item['Surface'] + "'" + "where url=" + "'" + item['Url'] + "'" + ";"
        self.cursor.execute(query)
        self.conn.commit()

