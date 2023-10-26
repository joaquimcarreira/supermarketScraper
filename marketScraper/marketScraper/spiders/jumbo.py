from scrapy import Spider
from scrapy.loader import ItemLoader
from marketScraper.items import TreeToUrlJumbo
from datetime import date
import json
import urllib.request


def get_ids(text):
    #return a matrix n x 2 where each row is a couple of ids and each column is a category and subcategory
    list = text.replace("true","True").replace("false","False")
    #convert from string to python language
    list = eval(list)
    ids_matrix = []
    #      [['1', '28'],
    #      ['1', '29'],
    #      [None, '1']]
    for parent0 in list[0:3]:
        if parent0["hasChildren"] == True:
            for children in parent0["children"]:
                ids_matrix.append([parent0["id"],children["id"]])
        else:
            ids_matrix.append([parent0["id"],None])
    return ids_matrix
     
def converter(data):
    #from the ids make urls to make the requests
    ids = get_ids(data)

    BASE = "https://www.jumbo.com.ar/api/catalog_system/pub/products/search/?fq=C%3a%2F"
    END = "%2F&O=OrderByScoreDESC&_from=0&_to=49"
    # create a list of urls with the ids obtained before
    urls = [(BASE + f'{id[0]}%2F{id[1]}' + END) if id[1] != None else (BASE + f'{id[0]}' + END) for id in ids] 

    return urls



class Arbol(Spider):
    name = "dataJumbo"
    # start Scrapping
    start_urls = [
        "https://www.jumbo.com.ar/api/catalog_system/pub/category/tree/2"
    ]
    custom_settings = {
        'FEED_URI': 'dataJumbo.json',
        'FEED_EXPORT_ENCODING': 'utf-8'
    }

    
    def parse(self,response):
        #get the tree where all the ids of the categories are
        text = response.xpath('//p/text()').get()    
        # call the function that returns the links to scrap
        links = converter(text)
        data = []
        #for every link make a request and filter the data
        for url in links[0:3]:
            #do the request 
            response = urllib.request.urlopen(url=url)
            #create a json with the data obtained
            json_response = json.load(response)            
            for product in json_response:
                #fitler the data I need
                price = product["items"][0]["sellers"][0]["commertialOffer"]["Price"]
                name = product["items"][0]["name"]
                categories = product["categories"][-1]
                day = date.today()
                product_data = {"date":day,"name":name,"categories":categories,"price":price}
                
                data.append(product_data)
        # return the data        
        yield {
            "data":data
        }
            
    

