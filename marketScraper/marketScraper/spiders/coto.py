from scrapy import Spider
import scrapy
from datetime import date
from marketScraper.items import MarketscraperItem
from scrapy.loader import ItemLoader


class Precios (Spider):
    name = "dataCoto"

    # Start Scraping

    start_urls = ["https://www.cotodigital3.com.ar/sitios/cdigi/"]
    #export savings
    custom_settings = {
        "FEEDS":{"dataCoto.json":{"format":"json"}},
        'FEED_EXPORT_ENCODING': 'utf-8'
    }


    def parse(self, response):
        # find all the links to scrap
        urls = response.xpath(
            '//div[@class="g1"]/ul[@class="sub_category"]/li/h2/a/@href').getall()
        BASE_URL = "https://www.cotodigital3.com.ar/"
        #make requests
        for url in urls[0:10]:
            yield scrapy.Request(BASE_URL + url, callback=self.parse_urls)

    # First scrap
    def parse_urls(self, response):
        today = date.today()

        def create_list(item):
            return [item for i in range(len(nombres)) ]
        # Xpath for prices, names and cateogories
        category = response.xpath('/html/head/title/text()').getall()
        price = response.xpath(
            '//div[@class="leftList"]/span[@class="atg_store_productPrice"]/span[@class="atg_store_newPrice"]/text()').getall()
        name = response.xpath(
            '//div[starts-with(@id,"descrip_full")]/text()').getall()
        
        # find the current page
        current_page = int(response.xpath(
            '//ul[@id="atg_store_pagination"]/li/a[@class="disabledLink"]/text()').get())
        # Given the current page, find the next one
        next_page = response.xpath(
            f'//ul[@id="atg_store_pagination"]/li/a[text()[contains(.,{current_page + 1})]]/@href').get()

        if next_page:
            # Get into the link of "next_page" and calls the func "parse_next_page"
            yield response.follow(next_page, callback=self.parse_next_pages, cb_kwargs={'categoria':categoria, 'precios': precios, 'nombres': nombres})
        else:
            # If no more pages are found, load the data and save it into an item for postProcess
            loader = ItemLoader(item=MarketscraperItem())
            loader.add_value("date",create_list(today))
            loader.add_value('categy', create_list(category[0]))
            loader.add_value('name', name)
            loader.add_value('price', price)
            yield loader.load_item()
    # Next page from the first one
    def parse_next_pages(self, response, **kwargs):
        #Create a list of categories if the same len of name and prices
        def create_list(item):
            return [item for i in range(len(nombres)) ]

        today = date.today()
        # Recieves data from the first page
        if kwargs:
            price = kwargs['price']
            name = kwargs['name']
            category = kwargs['category']

        # Extends what was obtained in the first page
        category.extend(response.xpath(
            '/html/head/title/text()').getall())
        price.extend(response.xpath(
            '//div[@class="leftList"]/span[@class="atg_store_productPrice"]/span[@class="atg_store_newPrice"]/text()').getall())
        name.extend(response.xpath(
            '//div[starts-with(@id,"descrip_full")]/text()').getall())

        current_page = int(response.xpath(
            '//ul[@id="atg_store_pagination"]/li/a[@class="disabledLink"]/text()').get())
        next_page = response.xpath(
            f'//ul[@id="atg_store_pagination"]/li/a[text()[contains(.,{current_page + 1})]]/@href').get()

        if next_page:
            # check and execute the next pages
            yield response.follow(next_page, callback=self.parse_next_pages, cb_kwargs={'category': category, 'price': price, 'name': name})
        else:
            # If no more pages are found, load the data and save it into an item for postProcess
            loader = ItemLoader(item=MarketscraperItem())
            loader.add_value("date",create_list(today))
            loader.add_value('category', create_list(category[0]))
            loader.add_value('name', name)
            loader.add_value('price', price)
            yield loader.load_item()