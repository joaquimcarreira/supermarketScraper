from scrapy import Spider
from marketScraper.items import MarketscraperItem, DiscountItem
from scrapy.loader import ItemLoader
import scrapy



class Ofertas(Spider):

    name = 'ofertasCoto'
    custom_settings = {
        'FEED_URI': 'ofertasCoto.json',
        'FEED_EXPORT_ENCODING': 'utf-8'
    }

    def start_requests(self):
        urls = [
            'https://www.cotodigital3.com.ar/sitios/cdigi/browse/categoria-ofertas/_/N-16uyom2#'
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parseDiscount)

    # La logica es la misma que "spider1.py"
    def parseDiscount(self, response):

        cantUnidades = response.xpath(
            '//div[@class="desc-llevandoN"]/text()').getall()
        porcentaje = response.xpath(
            '//div[@class="image_discount_container"]/span/text()').getall()
        precios = response.xpath(
            '//span[@class="price_discount"]//text()').getall()
        nombres = response.xpath(
            '//div[starts-with(@id,"descrip_full")]/text()').getall()

        current_page = int(response.xpath(
            '//ul[@id="atg_store_pagination"]/li/a[@class="disabledLink"]/text()').get())
        next_page = response.xpath(
            f'//ul[@id="atg_store_pagination"]/li/a[text()[contains(.,{current_page + 1})]]/@href').get()

        meta = {
            'cantUnidades': cantUnidades,
            'porcentaje': porcentaje,
            'precios': precios,
            'nombres': nombres
        }

        if next_page:
            yield response.follow(next_page, callback=self.parseDiscountNextPage, cb_kwargs=meta)

    def parseDiscountNextPage(self, response, **meta):
        cantUnidades = meta['cantUnidades']
        porcentaje = meta['porcentaje']
        precios = meta['precios']
        nombres = meta['nombres']

        cantUnidades.extend(
            response.xpath('//div[@class="desc-llevandoN"]/text()').getall()
        )
        porcentaje.extend(
            response.xpath(
                '//div[@class="image_discount_container"]/span/text()').getall()
        )
        precios.extend(
            response.xpath('//span[@class="price_discount"]//text()').getall()
        )
        nombres.extend(
            response.xpath(
                '//div[starts-with(@id,"descrip_full")]/text()').getall()

        )

        current_page = int(response.xpath(
            '//ul[@id="atg_store_pagination"]/li/a[@class="disabledLink"]/text()').get())
        next_page = response.xpath(
            f'//ul[@id="atg_store_pagination"]/li/a[text()[contains(.,{current_page + 1})]]/@href').get()

        if next_page:
            yield response.follow(next_page, callback=self.parseDiscountNextPage, cb_kwargs=meta)
        else:
            loader = ItemLoader(item=DiscountItem())
            loader.add_value('cantUnidades', cantUnidades)
            loader.add_value('porcentaje', porcentaje)
            loader.add_value('precios', precios)
            loader.add_value('nombres', nombres)
            yield loader.load_item()