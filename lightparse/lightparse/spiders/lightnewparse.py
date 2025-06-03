import scrapy


class LightnewparseSpider(scrapy.Spider):
    name = "lightnewparse"
    allowed_domains = ["divan.ru"]
    start_urls = ["https://www.divan.ru/category/svet"]

    def parse(self, response):
        lamps = response.css("div._Ud0k")
        for lamp in lamps:  #
            yield {
                "name": lamp.css("h2._Ud0k_ _title::text").get(),
                "price": lamp.css("span._Ud0k__price::text").get(),
                "link": lamp.css("a._Ud0k__link::attr(href)").get(),
            }
