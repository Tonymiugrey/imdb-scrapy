import scrapy
from imdbSpider.items import MovieItem


class MovieSpider(scrapy.Spider):
    name = "single"
    allowed_domains = ["imdb.com"]
    id_list_path = "conf/id-list"
    tmp_urls = []
    with open(id_list_path) as f:
        for line in f.readlines():
            tmp_urls.append("https://www.imdb.com/title/tt" + line)

    start_urls = tmp_urls

    def parse(self, response):
        item = MovieItem()
        item["title"] = response.xpath(
            '//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[1]/div[1]/h1/text()').extract()

        item["imdb_rating"] = response.xpath(
            '//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[1]/div[2]/div/'
            'div[1]/a/div/div/div[2]/div[1]/span[1]/text()').extract()

        item["popularity"] = response.xpath(
            '//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[1]/div[2]/div/'
            'div[3]/a/div/div/div[2]/div[1]/text()').extract()

        item["description"] = response.xpath(
            '//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[1]/div[1]/p/'
            'span[1]/text()').extract()

        item["imdb_id"] = [response.url.split("/")[-2]]
        tmp_link = response.xpath('//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[3]/'
                                  'div[1]/div/div[1]/div/a/@href').extract()
        if len(tmp_link) != 1:
            item["image_web_url"] = "Error"
            yield item
            return

        item['image_web_url'] = "https://www.imdb.com" + tmp_link[0].split('?')[0]
        yield scrapy.Request(item['image_web_url'], meta={'item': item}, callback=self.img_parse)

    def img_parse(self, response):
        item = response.meta['item']
        res = response.xpath('//*[@id="__next"]/main/div[2]/div[3]/div[4]/img/@src').extract()
        if len(res) != 1:
            yield item
            return
        item['image_urls'] = res
        yield item
