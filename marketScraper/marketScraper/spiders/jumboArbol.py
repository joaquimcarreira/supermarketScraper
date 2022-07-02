from scrapy import Spider
from scrapy.loader import ItemLoader
from marketScraper.items import TreeToUrlJumbo
import scrapy
import json

# Convierte los ids scrapeados en links
def converter(data):
    links = []    
    for i in range(len(data['ids'])):
        temp = [data['parentsLevel0'][i],data['parentsLevel1'][i]]
        if temp not in links:
            links.append(temp)
    # La matriz links tiene por fila la combinacion sin repetir de padres de cada id nivel2
    #      [['1', '28'],
    #      ['1', '29'],
    #      [None, '1']]

    # Entonces:
    BASE = "https://www.jumbo.com.ar/api/catalog_system/pub/products/search/?fq=C%3a%2F"
    END = "%2F&O=OrderByScoreDESC&_from=0&_to=49"
    urls = [(BASE + f'{link[0]}%2F{link[1]}' + END) if link[0] != None else (BASE + f'{link[1]}' + END) for link in links] 
        
    return urls


class Arbol(Spider):
    name = "dataJumbo"

    start_urls = [
        "https://www.jumbo.com.ar/api/catalog_system/pub/category/tree/2"
    ]
    custom_settings = {
        'FEED_URI': 'urlsJumbo.json',
        'FEED_EXPORT_ENCODING': 'utf-8'
    }

    
    def parse(self,response):
        # obtengo ids nivel2
        ids = response.xpath('//CategoryTree[HasChildren="false"]/Id/text()').getall()
        # para cada id nivel2 obtengo una lista de sus padres
        parentsLevel1 = [response.xpath(f'//CategoryTree[Id={id}]/FatherCategoryId/text()').get() for id in ids]
        parentsLevel0 = [response.xpath(f'//CategoryTree[Id={id}]/FatherCategoryId/text()').get() for id in parentsLevel1]
        

        ids = {
            'ids':ids,
            'parentsLevel1':parentsLevel1,
            'parentsLevel0':parentsLevel0
        }

        links = converter(ids)
        
        for url in links:
            yield scrapy.Request(url=url,callback=self.parseUrl)
    
    def parseUrl(self,response):
        result = json.loads(response.body)
        yield {
            "result":result
        } 