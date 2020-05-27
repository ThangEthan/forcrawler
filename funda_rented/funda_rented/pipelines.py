
# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import mysql.connector


class FundaRentedPipeline(object):
    def __init__(self):
        self.create_connection()

    def create_connection(self):
        self.conn = mysql.connector.connect(
            host='192.168.178.11',
            user='root',
            passwd='thang1998',
            database='scraping_data')
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        self.update_db(item)
        return item

    def update_db(self, item):

        query = "UPDATE fundarent SET "

        for i in item.keys():
            if i != 'Url':
                if item[i] != None:
                    query = query + i + " = '" + \
                        item[i].strip().replace("\n", "").replace(
                            "\t", "").replace("'", '"').strip() + "'" + ","
                else:
                    query = query + "'',"
        query = query[0:-1] + " WHERE Url='" + item['Url'] + "';"
        print(query)
        self.cursor.execute(query)
        self.conn.commit()
