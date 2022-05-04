# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ImdbspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class MovieItem(scrapy.Item):
    title = scrapy.Field()
    rating = scrapy.Field()
    popularity = scrapy.Field()
    description = scrapy.Field()
    image_url = scrapy.Field()
    imdb_url = scrapy.Field()


class NewMovie(scrapy.Item):
    imdb_url = scrapy.Field()
    imdb_id = scrapy.Field()
    title = scrapy.Field()
    rating = scrapy.Field()
    popularity = scrapy.Field()
    year = scrapy.Field()
    release_time = scrapy.Field()
    image_url = scrapy.Field()
    description = scrapy.Field()


class FavouriteItem(scrapy.Item):
    imdb_url = scrapy.Field()
    imdb_id = scrapy.Field()
    title = scrapy.Field()
    rating = scrapy.Field()
    popularity = scrapy.Field()
    year = scrapy.Field()
    release_time = scrapy.Field()
    image_url = scrapy.Field()
    rank = scrapy.Field()
    image_web_url = scrapy.Field()
    description = scrapy.Field()