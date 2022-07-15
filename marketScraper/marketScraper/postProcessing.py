from importlib.resources import path
import json
import os
from os.path import exists

class PostProcess():
    '''
    Modify the data scraped and shape it for future analisys
    '''
    def __init__(self,path,output_path="marketScraper/data/precios.json") -> None:
        self.path = path       
        self.output_path = output_path
    def process(self,delete=False):
        # open file and load json
        with open(self.path,"r") as f:
            data = json.load(f)
        if (exists(self.output_path)):
            with open(self.output_path,"r") as of:
                self.dict_data = json.load(of)
        else:
            # create an empty dict with the same keys as data
            self.dict_data = {key:list() for key in data[0].keys()}
        for i in data:
            for key,_ in self.dict_data.items():
                # limit the len of the list
                # modify the dict shape for better reading 
                self.dict_data[key].extend(i[key][:len(i["precios"])])
    
        with open(self.output_path,"w") as f:
            json.dump(self.dict_data,f) 
        print("************************")     
        print("File created succesfully")
        print("************************")
        if delete==True:
            os.remove(path)

proceso = PostProcess(path="/home/joaquim/Proyectos/marketScrapper/marketScraper/preciosCoto.json")
proceso.process(delete=True)

    



