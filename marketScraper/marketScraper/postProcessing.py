import json
# with open("preciosCoto.json","r") as f:
#     data = json.load(f)

class PostProcess():
    '''
    Modify the data scraped and shape it for future analisys
    '''
    def __init__(self,path) -> None:
        self.path = path
    def process(self):
        # open file and load json
        with open(self.path,"r") as f:
            data = json.load(f)
        # create an empty dict with the same keys as data
        self.dict_data = {key:list() for key in data[0].keys()}
        for i in data:
            for key,_ in self.dict_data.items():
                # limit the len of the list
                # modify the dict shape for better reading 
                self.dict_data[key].extend(i[key][:len(i["precios"])])
    def create_file(self,path,name):
        with open(path + "/" + name,"w") as f:
            json.dump(self.dict_data,f) 
        print("************************")     
        print("File created succesfully")
        print("************************")

proceso = PostProcess("preciosCoto.json")
proceso.process()
proceso.create_file("marketScraper/data","precios.json")
    



