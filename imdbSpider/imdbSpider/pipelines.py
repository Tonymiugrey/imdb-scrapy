# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import csv

import scrapy
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem


class ImdbspiderPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            yield scrapy.Request(image_url)

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        item['image_paths'] = image_paths
        return item


class ListCsvPipeline(object):
    def __init__(self):
        self.f = open("data/list.csv", "w", newline="", encoding="utf-8")
        self.fieldnames = ["title", "description",  "image_url", "imdb_url", "rating", "popularity"]
        self.writer = csv.DictWriter(self.f, fieldnames=self.fieldnames)
        self.writer.writeheader()

    def process_item(self, item, spider):
        if spider.name == "list":
            print(item)
        self.writer.writerow(item)
        return item

    def close(self, spider):
        self.f.close()


class FavouriteCsvPipeline(object):
    def __init__(self):
        self.f = open("data/favourite.csv", "w", newline="")
        self.fieldnames = ["title", "description",  "image_url", "imdb_url", "rating", "popularity", "year"]
        self.writer = csv.DictWriter(self.f, fieldnames=self.fieldnames)
        self.writer.writeheader()

    def process_item(self, item, spider):
        if spider.name == "favourite":
            print(item)
        self.writer.writerow(item)
        return item

    def close(self, spider):
        self.f.close()


class NewCsvPipeline(object):
    def __init__(self):
        self.f = open("data/new.csv", "w", newline="")
        self.fieldnames = ["title", "description",  "image_url", "imdb_url", "rating", "popularity", "release_time"]
        self.writer = csv.DictWriter(self.f, fieldnames=self.fieldnames)
        self.writer.writeheader()

    def process_item(self, item, spider):
        if spider.name == "new":
            print(item)
        self.writer.writerow(item)
        return item

    def close(self, spider):
        self.f.close()
