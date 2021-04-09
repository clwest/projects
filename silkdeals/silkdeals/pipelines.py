# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import logging
import sqlite3


class SQLlitePipeLine(object):
    
    def open_spider(self, spider):
        self.connection = sqlite3.connect("slickdeals.db")
        self.c = self.connection.cursor()
        try:
            self.c.execute(''' 
                CREATE TABLE cheap_comps(
                    name TEXT,
                    link TEXT,
                    store_name TEXT,
                    price TEXT
                    
                )
            ''')
            self.connection.commit()
        except sqlite3.OperationalError:
            pass


    def close_spider(self, spider):
        self.connection.close()



    def process_item(self, item, spider):
        self.c.execute(''' 
            INSERT INTO cheap_comps (name, link, store_name, price) VALUES(?,?,?,?)

        ''',(
            item.get('name'),
            item.get('link'),
            item.get('store_name'),
            item.get('price')
        ))
        self.connection.commit()
        return item
