import scrapy


class LightnewparseSpider(scrapy.Spider):
    name = "lightnewparse"
    allowed_domains = ["divan.ru"]
    start_urls = ["https://www.divan.ru/category/svet"]

    def parse(self, response):
        # 1. Проходим по всем карточкам товара (у каждой есть класс "_Ud0k")
        for lamp in response.css("div._Ud0k"):
            # 2. Название лежит в <span itemprop="name">…</span>
            name = lamp.css("span[itemprop='name']::text").get()

            # 3. Цена. Чаще всего берут первое вхождение data-testid="price".
            #    Это вернёт строку вида "4990" (по умолчанию без "руб.")
            price = lamp.css("span.KIkOH[data-testid='price']::text").get()

            # 4. Ссылка на товар. У тега <a> с классом ProductName есть href="/product/..."
            relative_url = lamp.css("a.ProductName::attr(href)").get()
            #    Если ссылок несколько, .get() выдаст первую.
            #    Например: "/product/podvesnoj-svetilnik-ferum-orange"
            #    Собираем абсолютный URL:
            detail_url = response.urljoin(relative_url) if relative_url else None

            # 5. Теперь «yield»им результат
            yield {
                "name": name,
                "price": price,
                "detail_url": detail_url
            }

#<span class="ui-LD-ZU KIkOH" data-testid="price">4990<span class="ui-i5wwi ui-VDyJR ui-VWOa-">руб.</span></span>