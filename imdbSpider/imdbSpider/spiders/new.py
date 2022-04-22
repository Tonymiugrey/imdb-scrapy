import scrapy
from imdbSpider.items import NewMovie


class NewMovieSpider(scrapy.Spider):
    name = "new"
    allowed_domains = []
    start_urls = [
        "https://www.imdb.com/calendar/"
    ]

    def parse(self, response):
        """
        用以处理主题贴的首页
        :param response:
        :return:
        """
        # date group

        item = NewMovie()
        date_list = response.xpath('//*[@id="main"]/h4/text()').extract()
        i = 1
        for date in date_list:
            nums = len(response.xpath('//*[@id="main"]/ul[' + str(i) + ']/li'))
            for j in range(1, nums+1):
                item = NewMovie()
                item['date'] = date
                temp_xpath = '//*[@id="main"]/ul[' + str(i) + ']/li[' + str(j) + ']'
                title_name = response.xpath(temp_xpath + '/a/text()').extract()
                if len(title_name) != 1:
                    item['title'] = "Error: title name length is 0"
                    yield item
                    continue

                title_year = response.xpath(temp_xpath + '/text()').extract()
                if  len(title_year) != 2:
                    item['title'] = "Error: title year length is 0"
                    yield item
                    continue
                title_year = title_year[-1].split('\n')[0]
                item['title'] = title_name[0] + title_year[0]

                tmp_link = response.xpath(temp_xpath + '/a/@href')
                if len(tmp_link) != 1:
                    item['link'] = "Error: link length is 0"
                    yield item
                    continue
                tmp_link = tmp_link.extract()[0].split('?')[0]
                item['link'] = 'https://www.imdb.com' + tmp_link

                item['imdb_id'] = item['link'].split('/')[-2]

                yield scrapy.Request(item['link'], meta={'item': item}, callback=self.popularity_parse)
            i = i + 1

    def popularity_parse(self, response):
        item = response.meta['item']
        res = response.xpath('//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[1]/div[2]/div/div/a/div/div/div[2]/div[1]/text()').extract()
        if len(res) != 1:
            item['popularity'] = "None"
            yield item
            return
        item['popularity'] = res[0]
        yield item


