
# %%
import pandas as pd
import json
# %%
with open("../preciosCoto.json","r") as f:
    # json_data = [json.loads(line) for line in f]
    data = json.load(f)
data
#%%
keys = ["date","categoria","nombres","precios"]

data[14]["categoria"]
# %%
for i in range(len(data)):
    for n in keys:
        print(i,n,len(data[i][n]),data[i]["categoria"][0])    
    print()
#%%

dict_data = {"date":list(),
        "categoria":list(),
        "nombres":list(),
        "precios":list()}

data = pd.DataFrame(columns=df.columns)
data
#%%
for key,value in dict_data.items():
    print(len([i for n in json_data for i in n[key]]))




# %%
for column in df.columns:
    for index, row in df.iterrows():
        print(len(df[column].iloc[index]))
# %%
for index,row in df[["precios"]].iterrows():
    print(index,row)
# %%
df
# %%
