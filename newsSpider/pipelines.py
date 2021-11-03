# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from datetime import datetime
from itemadapter import ItemAdapter
from scrapy.exporters import JsonItemExporter

class GuardianSpiderPipeline:
    def process_item(self, item, spider):
        item.setdefault('source', 'Guardian')
        return item

class SMHSpiderPipeline:
    def process_item(self, item, spider):
        item.setdefault('source', 'SMH')
        return item


class NewsSpiderPipeline:

    def __init__(self):
        self.exporter = None
        self.file = None

    def open_spider(self, spider):
        timeStamp = datetime.now().strftime("%Y-%m-%d_%H%M")
        self.file = open(f'output/{spider.name}_{timeStamp}.json', 'w+b')
        json_exporter = JsonItemExporter(file = self.file, indent = 0)
        json_exporter.start_exporting()
        self.exporter = json_exporter


    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item
