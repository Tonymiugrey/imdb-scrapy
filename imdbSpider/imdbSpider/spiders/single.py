import scrapy
from imdbSpider.items import MovieItem


class MovieSpider(scrapy.Spider):
    name = "single"
    allowed_domains = ["https://www.imdb.com/"]
    start_urls = [
        "https://www.imdb.com/title/tt10048342/"
    ]

    def parse(self, response):
        movie_item = MovieItem()
        movie_item["title"] = response.xpath(
            '//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[1]/div[1]/h1/text()').extract()

        movie_item["imdb_rating"] = response.xpath(
            '//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[1]/div[2]/div/'
            'div[1]/a/div/div/div[2]/div[1]/span[1]/text()').extract()

        movie_item["popularity"] = response.xpath(
            '//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[1]/div[2]/div/'
            'div[3]/a/div/div/div[2]/div[1]/text()').extract()

        movie_item["description"] = response.xpath(
            '//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[1]/div[1]/p/'
            'span[1]/text()').extract()

        movie_item["imdb_id"] = [response.url.split("/")[-2]]
        yield movie_item
