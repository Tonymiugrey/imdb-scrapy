import scrapy
from ..items import FavouriteItem
from tqdm import tqdm

class FavouriteSpider(scrapy.Spider):
    name = "favourite"
    allowed_domains = ["www.imdb.com"]
    start_urls = [
        "https://www.imdb.com/chart/moviemeter/"
    ]
    custom_settings = {
        "ITEM_PIPELINES": {"imdbSpider.pipelines.FavouriteCsvPipeline": 400},
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        'Accept-Language': 'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4',
        'Cookie': 'uu=eyJpZCI6InV1ODI1NGNhNWJkMjRmNDI1ZTkzMzUiLCJwcmVmZXJlbmNlcyI6eyJmaW5kX2luY2x1ZGVfYWR1bHQiOmZhbHNlfX0=; '
                  'session-id=132-7557577-7889513; adblk=adblk_no; ubid-main=133-7010020-4267562; session-id-time=2082787201l; '
                  'session-token=BXdPrVQGbVhAe133Ka/lEF5hZaY6SbRz33zZUoKgxOEHI9ioAOBfNNibYn0krX0ttwRtJkQbGjbWMSgF0PuPRAbOSR2V7sF'
                  'ODjsrRoyjTfMzMXvP0qkloFVLLzNiApSo1TnG+p++Wc2qQNvF3EwIbvdwB8byPWXsWecBZJYpGZXFr8EvtOolfLw+6dPaPHuh; '
                  'csm-hit=tb:s-K8HKPJAH2ZWA1GFHQTYE|1651125536001&t:1651125536273&adb:adblk_no'
    }

    def parse(self, response):
        for i in range(1, 101):
            # need to check popularity
            item = FavouriteItem()
            xpath = '//*[@id="main"]/div/span/div/div/div[3]/table/tbody/tr[' + str(i) + ']'
            movie_name = response.xpath(xpath + '/td[2]/a/text()').extract()[0]
            movie_year = response.xpath(xpath + '/td[2]/span/text()').extract()
            if len(movie_year) != 0:
                movie_year = movie_year[0].split('(')[1].split(')')[0]
            else:
                movie_year = ""
            tmp_link_id = response.xpath(xpath + '/td[2]/a/@href').extract()[0]

            # item['imdb_id'] = tmp_link_id.split('/')[-2].split('tt')[1]
            item['title'] = movie_name + '(' + movie_year + ')'
            item['rating'] = response.xpath(xpath + '/td[3]/strong/text()').extract()
            if len(item['rating']) == 1:
                item['rating'] = item['rating'][0]
            else:
                item['rating'] = None
            item['popularity'] = str(i)
            item['year'] = movie_year
            item['imdb_url'] = 'https://www.imdb.com' + tmp_link_id
            # yield item
            yield scrapy.Request(item['imdb_url'], meta={'item': item}, callback=self.parse_image_web_url, headers=self.headers)

    def parse_image_web_url(self, response):
        item = response.meta['item']
        src = response.xpath('//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[3]/div[1]/div/div[1]/div/a/@href').extract()
        item["description"] = response.xpath(
            '//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[1]/div[1]/p/'
            'span[1]/text()').extract()
        item["description"] = item["description"][0] if len(item["description"]) != 0 else ""
        if len(src) != 0:
            image_web_url = "https://www.imdb.com" + src[0].split('?')[0]
            yield scrapy.Request(image_web_url, meta={'item': item}, callback=self.parse_image_url, headers=self.headers)
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
