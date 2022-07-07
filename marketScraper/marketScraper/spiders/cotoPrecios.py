from venv import create
from scrapy import Spider
import scrapy
from datetime import date
from marketScraper.items import MarketscraperItem
from scrapy.loader import ItemLoader


class Precios (Spider):
    name = "preciosCoto"

    # Comienzo de scrapeo

    start_urls = ["https://www.cotodigital3.com.ar/sitios/cdigi/"]

    custom_settings = {
        "FEEDS":{"preciosCoto.json":{"format":"json"}},
        'FEED_EXPORT_ENCODING': 'utf-8'
    }


    def parse(self, response):
        # encuentra todos los links a scrapear de la pagina
        urls = response.xpath(
            '//div[@class="g1"]/ul[@class="sub_category"]/li/h2/a/@href').getall()
        BASE_URL = "https://www.cotodigital3.com.ar/"
        for url in urls[0:15]:
            yield scrapy.Request(BASE_URL + url, callback=self.parse_urls)

    # Primera pagina
    def parse_urls(self, response):

        def create_list(self,item):
            return [item for i in range(len(nombres)) ]
        # Xpath para precios, nombres y categoria
        categoria = response.xpath('/html/head/title/text()').getall()
        precios = response.xpath(
            '//div[@class="leftList"]/span[@class="atg_store_productPrice"]/span[@class="atg_store_newPrice"]/text()').getall()
        nombres = response.xpath(
            '//div[starts-with(@id,"descrip_full")]/text()').getall()

        # Encuentra la pagina actualz
        current_page = int(response.xpath(
            '//ul[@id="atg_store_pagination"]/li/a[@class="disabledLink"]/text()').get())
        # Segun la pagina actual, obtiene el link de la pagina siguiente
        next_page = response.xpath(
            f'//ul[@id="atg_store_pagination"]/li/a[text()[contains(.,{current_page + 1})]]/@href').get()

        if next_page:
            # Entra en el link de "next_page" y llama a la funcion "parse_next_pages"
            yield response.follow(next_page, callback=self.parse_next_pages, cb_kwargs={'categoria':categoria, 'precios': precios, 'nombres': nombres})
        else:
            # cunado no hay mas paginas, se carga lo encontrado y se lo guarda en item para el postprocesado
            loader = ItemLoader(item=MarketscraperItem())
            loader.add_value("date",create_list(today))
            loader.add_value('categoria', create_list(categoria[0]))
            loader.add_value('nombres', nombres)
            loader.add_value('precios', precios)
            yield loader.load_item()
    # Paginas siguientes a la primera
    def parse_next_pages(self, response, **kwargs):
        # crea una lista de categorias de la misma len de nombre y precios
        def create_list(item):
            return [item for i in range(len(nombres)) ]

        today = date.today()
        # recibe lo obtenido de la primer pagina
        if kwargs:
            precios = kwargs['precios']
            nombres = kwargs['nombres']
            categoria = kwargs['categoria']

        # extiendo lo obetino de la primer pagina
        categoria.extend(response.xpath(
            '/html/head/title/text()').getall())
        precios.extend(response.xpath(
            '//div[@class="leftList"]/span[@class="atg_store_productPrice"]/span[@class="atg_store_newPrice"]/text()').getall())
        nombres.extend(response.xpath(
            '//div[starts-with(@id,"descrip_full")]/text()').getall())

        current_page = int(response.xpath(
            '//ul[@id="atg_store_pagination"]/li/a[@class="disabledLink"]/text()').get())
        next_page = response.xpath(
            f'//ul[@id="atg_store_pagination"]/li/a[text()[contains(.,{current_page + 1})]]/@href').get()

        if next_page:
            # checkeo y ejecucion de paginas siguientes
            yield response.follow(next_page, callback=self.parse_next_pages, cb_kwargs={'categoria': categoria, 'precios': precios, 'nombres': nombres})
        else:
            # cunado no hay mas paginas, se carga lo encontrado y se lo guarda en item para el postprocesado
            loader = ItemLoader(item=MarketscraperItem())
            loader.add_value("date",create_list(today))
            loader.add_value('categoria', create_list(categoria[0]))
            loader.add_value('nombres', nombres)
            loader.add_value('precios', precios)
            yield loader.load_item()