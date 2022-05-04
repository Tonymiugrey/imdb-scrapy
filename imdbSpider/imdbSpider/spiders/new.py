import scrapy
from ..items import NewMovie


class NewMovieSpider(scrapy.Spider):
    name = "new"
    allowed_domains = []
    start_urls = [
        "https://www.imdb.com/calendar/"
    ]
    custom_settings = {
        "ITEM_PIPELINES": {"imdbSpider.pipelines.NewCsvPipeline": 400},
    }

    def parse(self, response):
        date_list = response.xpath('//*[@id="main"]/h4/text()').extract()
        i = 1
        for date in date_list:
            nums = len(response.xpath('//*[@id="main"]/ul[' + str(i) + ']/li'))
            for j in range(1, nums+1):
                item = NewMovie()
                temp_xpath = '//*[@id="main"]/ul[' + str(i) + ']/li[' + str(j) + ']'
                title_name = response.xpath(temp_xpath + '/a/text()').extract()
                if len(title_name) != 1:
                    item['title'] = "Error: title name length is 0"
                    yield item
                    continue

                title_year = response.xpath(temp_xpath + '/text()').extract()
                if len(title_year) != 2:
                    item['title'] = "Error: title year length is 0"
                    yield item
                    continue
                title_year = title_year[-1].split('\n')[0]
                tmp_link = response.xpath(temp_xpath + '/a/@href')
                if len(tmp_link) != 1:
                    item['image_url'] = "Error: link length is 0"
                    yield item
                    continue
                tmp_link = tmp_link.extract()[0].split('?')[0]

                # release_time
                item['release_time'] = date
                # title
                item['title'] = title_name[0] + title_year[0]
                # imdb_id
                # item['imdb_id'] = tmp_link.split('/')[2].split('tt')[1]
                item['imdb_url'] = 'https://www.imdb.com' + tmp_link
                yield scrapy.Request(item['imdb_url'], meta={'item': item}, callback=self.movie_parse)
            i = i + 1
        print(i)

    def movie_parse(self, response):
        item = response.meta['item']
        popularity = response.xpath('//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[1]/div[2]/div/div/a/div/div/div[2]/div[1]/text()').extract()
        item["description"] = response.xpath(
            '//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[1]/div[1]/p/'
            'span[1]/text()').extract()
        item["description"] = item["description"][0] if len(item["description"]) != 0 else ""
        if len(popularity) == 0:
            item['popularity'] = "None"
            yield item
            return
        # popularity
        item['popularity'] = popularity[0]
        rating = response.xpath(
            '//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[1]/div[2]/div/'
            'div[1]/a/div/div/div[2]/div[1]/span[1]/text()').extract()
        # rating
        item['rating'] = rating[0] if len(rating)!=0 else ""
        year = response.xpath('//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[1]/div[1]'
                              '/div/ul/li[1]/a/text()').extract()
        # year
        # if len(year) == 0:
        #     item['year'] = ""
        # else:
        #     item['year'] = year[0]
        src = response.xpath(
            '//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[3]/div[1]/div/div[1]/div/a/@href').extract()
        if len(src) != 0:
            image_web_url = "https://www.imdb.com" + src[0].split('?')[0]
            yield scrapy.Request(image_web_url, meta={'item': item}, callback=self.parse_image_url)
        else:
            item['image_url'] = ""
            yield item

    def parse_image_url(self, response):
        item = response.meta['item']
        src = response.xpath('//*[@id="__next"]/main/div[2]/div[3]/div[4]/img/@src').extract()
        if len(src) != 0:
            item['image_url'] = src[0]
        else:
            item['image_url'] = "None"
        yield item


