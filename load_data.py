import requests, json
import numpy as np
import pandas as pd
from pandas.io.json import json_normalize
import datetime

url = 'https://www.mohfw.gov.in/data/datanew.json'
res = requests.get(url)

with open("data.json", "w") as f:
    json.dump(res.json(), f)

with open("data.json") as f:
    data = json.load(f)
df_in = pd.DataFrame.from_dict(pd.json_normalize(data), orient='columns')


df = df_in.drop(['sno','new_active', 'new_positive', 'new_cured', 'new_death', 'state_code'], axis = 1)

'''dropping unnecessary rows containing below words/characters'''
df['state_name'].replace('', np.nan, inplace = True)
df.dropna(subset =['state_name'], inplace = True)

'''adding date column with value today'''
df['Date'] = datetime.date.today()

df.rename(columns={"positive": "Confirmed"}, inplace= True)

print(df)