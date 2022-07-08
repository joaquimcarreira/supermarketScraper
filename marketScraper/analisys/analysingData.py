
# %%
import pandas as pd
import json

with open("../preciosCoto.json","r") as f:
    data = json.load(f)

dict_data = {key:list() for key in data[0].keys()}

for i in data:
    for key,value in dict_data.items():
        dict_data[key].extend(i[key][:len(i["precios"])])

df = pd.DataFrame(dict_data)



# %%
