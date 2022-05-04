import scrapy
from ..items import MovieItem


class MovieSpider(scrapy.Spider):
    name = "list"
    allowed_domains = ["imdb.com"]
    id_list_path = "conf/imdb-url-list"
    tmp_urls = []
    with open(id_list_path) as f:
        for line in f.readlines():
            tmp_urls.append(line)

    start_urls = tmp_urls
    custom_settings = {
        "ITEM_PIPELINES": {"imdbSpider.pipelines.ListCsvPipeline": 400},
    }

    def parse(self, response):
        item = MovieItem()
        title= response.xpath(
            '//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[1]/div[1]/h1/text()').extract()
        item["title"] = title[0] if len(title) != 0 else ""

        rating = response.xpath(
            '//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[1]/div[2]/div/'
            'div[1]/a/div/div/div[2]/div[1]/span[1]/text()').extract()
        item["rating"] = rating[0] if len(rating) != 0 else ""

        popularity = response.xpath(
            '//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[1]/div[2]/div/'
            'div[3]/a/div/div/div[2]/div[1]/text()').extract()
        item["popularity"] = popularity[0] if len(popularity) != 0 else ""

        description = response.xpath(
            '//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[1]/div[1]/p/'
            'span[1]/text()').extract()
        item["description"] = description[0] if len(description) != 0 else ""

        item["imdb_url"] = response.url

        # item["imdb_id"] = [response.url.split("/")[-2]]
        tmp_link = response.xpath('//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[3]/'
                                  'div[1]/div/div[1]/div/a/@href').extract()
        if len(tmp_link) != 1:
            yield item
            return

        image_web_url = "https://www.imdb.com" + tmp_link[0].split('?')[0]
        yield scrapy.Request(image_web_url, meta={'item': item}, callback=self.img_parse)

    def img_parse(self, response):
        item = response.meta['item']
        res = response.xpath('//*[@id="__next"]/main/div[2]/div[3]/div[4]/img/@src').extract()
        if len(res) != 1:
            yield item
            return
        image_url = res
        item['image_url'] = image_url[0] if len(image_url) != 0 else ""
        yield item
