# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json


class JobscrapePipeline:
    def process_item(self, item, spider):
        return item


class JsonWriterPipeline:
    def __init__(self):
        self.file = open("jobs.json", "w", encoding="utf-8")
        self.file.write("[\n")  # Start JSON array

    def close_spider(self, spider):
        self.file.write("\n]")  # Close JSON array
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + ",\n"  # Convert item to JSON and add a comma
        self.file.write(line)
        self.file.flush() 
        return item
