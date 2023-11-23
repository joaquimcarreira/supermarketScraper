import scrapy
from scrapy import Spider
from scrapy.loader import ItemLoader
from marketScraper.items import BancosCoto


class Bancos(Spider):
    name = "cotoBancos"

    start_urls = [
        "https://www.cotodigital3.com.ar/sitios/cdigi/promo/promotions.jsp"
        ]
    custom_settings = {
        'FEED_URI': 'descuentosCoto.json',
        'FEED_EXPORT_ENCODING': 'utf-8'
    }

    def parse(self,response):
        nombre = response.xpath('//ul[@id="Grid"]/li/center/div[@class="desc_bank_img"]/img/@src').extract()
        descuento =  response.xpath('//ul[@id="Grid"]/li/div[@class="desc_numero"]/text()').extract()
        dias =  response.xpath('//ul[@id="Grid"]/li/div[@class="desc_days"]/text()').extract() 
        condicion1 =  response.xpath('//ul[@id="Grid"]/li/center/div[@class="desc_info"]/text()').extract()
        condicion2 =  response.xpath('//ul[@id="Grid"]/li/center/div[@class="desc_info_condiciones"]/text()').extract()

        condicionTotal = [condicion1[i]+condicion2[i] for i in range(len(condicion1))]


        loader = ItemLoader(item=BancosCoto())
        loader.add_value('nombre',nombre)
        loader.add_value('dia',dias)
        loader.add_value('condiciones',condicionTotal)
        loader.add_value('descuento',descuento)
        yield loader.load_item()
        

