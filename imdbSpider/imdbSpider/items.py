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
    imdb_rating = scrapy.Field()
    popularity = scrapy.Field()
    description = scrapy.Field()
    imdb_id = scrapy.Field()


class NewMovie(scrapy.Item):
    date = scrapy.Field()
    title = scrapy.Field()
    popularity = scrapy.Field()
    imdb_id = scrapy.Field()
    link = scrapy.Field()

class FavouriteItem(scrapy.Item):
    title = scrapy.Field()
    rank = scrapy.Field()
    imdb_rating = scrapy.Field()
    imdb_id = scrapy.Field()
    link = scrapy.Field()
    popularity = scrapy.Field()
