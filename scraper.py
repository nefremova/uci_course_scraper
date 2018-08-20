import scrapy

class CatalogSpider(scrapy.Spider):
    name = "catalog_spider"
    start_urls = ['http://catalogue.uci.edu/donaldbrenschoolofinformationandcomputersciences/departmentofcomputerscience/#majorstext']

    def parse(self, response):
        COURSE_SELECTOR = '.codecol'
        for course in response.css(COURSE_SELECTOR):
            NEXT_PAGE_SELECTOR = 'div a::attr(href)'
            next_page = course.css(NEXT_PAGE_SELECTOR).extract_first()

            if next_page:
                url = 'http://catalogue.uci.edu' + next_page
                yield scrapy.Request(url, callback = self.parse_details)
            else:
                yield None

    def parse_details(self, response):
        COURSE_INFO_SELECTOR = '.searchresult h2::text'

        yield {
            'info' : response.css(COURSE_INFO_SELECTOR).extract_first()
        }
