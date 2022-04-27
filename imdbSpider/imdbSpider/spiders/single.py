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
        # basic info
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
        item['count'] = 0
        yield scrapy.Request(item['image_web_url'], meta={'item': item}, callback=self.img_step1())

    def img_step1(self, response):
        item = response.meta['item']
        flag = response.xpath('//*[@id="__next"]/main/div[2]/div[3]/div[6]/div/div/div/div[1]/'
                              'span[2]/text()').extract()[0].split(' of ')[0]
        flag = int(flag)
        # 图库一页有48张
        page = int(flag / 48) + 1
        item['tmp_value'] = flag % 48
        item['tmp_url'] = 'https://www.imdb.com/title/tt5180504/mediaindex?page=' + str(page)
        yield scrapy.Request(item['image_tmp_url'], meta={'item': item}, callback=self.img_step2)

    def img_step2(self, response):
        item = response.meta['item']
        count = item['tmp_value']
        for i in range(count, count+6):
            item['image_web_url'] = response.xpath('//*[@id="media_index_thumbnail_grid"]/a[' + str(count) +']/@href').extract()[0].split('?')[0]
            yield scrapy.Request(item['image_tmp_url'], meta={'item': item}, callback=self.download_image)

    def download_image(self, response):
        item = response.meta['item']
        item['tmp_url'] = response.xpath('//*[@id="__next"]/main/div[2]/div[3]/div[4]/img/@src').extract()[0]
        yield item



