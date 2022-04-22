import scrapy
from imdbSpider.items import FavouriteItem


class FavouriteSpider(scrapy.Spider):
    name = "favourite"
    allowed_domains = ["https://www.imdb.com/chart/moviemeter/"]
    start_urls = [
        "https://www.imdb.com/chart/moviemeter/"
    ]

    def parse(self, response):
        for i in range(1, 101):
            # need to check popularity
            item = FavouriteItem()
            xpath = '//*[@id="main"]/div/span/div/div/div[3]/table/tbody/tr[' + str(i) + ']'
            movie_name = response.xpath(xpath + '/td[2]/a/text()').extract()[0]
            movie_year = response.xpath(xpath + '/td[2]/span/text()').extract()[0]
            item['title'] = movie_name + movie_year

            item['imdb_rating'] = response.xpath(xpath + '/td[3]/strong/text()').extract()
            item['rank'] = i
            item['popularity'] = i
            tmp_link_id = response.xpath(xpath + '/td[2]/a/@href').extract()[0]
            item['link'] = 'https://www.imdb.com/' + tmp_link_id
            item['imdb_id'] = tmp_link_id.split('/')[-2]
            yield item
