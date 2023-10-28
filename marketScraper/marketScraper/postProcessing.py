from importlib.resources import path
import json
import os
from os.path import exists

class PostProcess():
    '''
    Modify the data scraped and shape it for future analisys
    '''
    def __init__(self,path,output_path,supermarket) -> None:
        self.path = path       
        self.output_path = output_path
        self.supermarket = supermarket
    def process(self,delete=False):
        # open file and load json
        # each supermarket requires different post process
        with open(self.path,"r") as f:
            if self.supermarket=="coto":
                data = json.load(f)
            elif self.supermarket=="jumbo":
                data = json.load(f)["data"]
        if (exists(self.output_path)):
            with open(self.output_path,"r") as of:
                self.dict_data = json.load(of)
        else:
            # create an empty dict with the same keys as data
            self.dict_data = {key:list() for key in data[0].keys()}
        for i in data:
            for key,_ in self.dict_data.items():
                # modify the dict shape for better reading 
                if self.supermarket=="coto":
                    # limit the len of the list
                    self.dict_data[key].extend(i[key][:len(i["precios"])])
                elif self.supermarket=="jumbo":
                    self.dict_data[key].append(i[key])
                    
        # save the file 
        with open(self.output_path,"w") as f:
            json.dump(self.dict_data,f) 
        print("************************")     
        print("File created succesfully")
        print("************************")
        #delete the original data after process
        if delete==True:
            os.remove(self.path)
PATH_COTO = "../marketScraper/dataCoto.json"
OUTPATH_COTO = "../marketScraper/marketScraper/data/dataCOTO.json"
procesoCoto = PostProcess(path=PATH_COTO,output_path=OUTPATH_COTO,supermarket="coto")
#procesoCoto.process(delete=True)
path_JUMBO = "../marketScraper/dataJumbo.json"
OUTPATH_JUMBO = "../marketScraper/marketScraper/data/dataJUMBO.json"
procesoJumbo = PostProcess(path=path_JUMBO,output_path=OUTPATH_JUMBO,supermarket="jumbo")
procesoJumbo.process(delete=True)


    



