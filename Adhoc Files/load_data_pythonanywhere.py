import requests, json
import numpy as np
import pandas as pd
from pandas.io.json import json_normalize
import datetime

url = 'https://www.mohfw.gov.in/data/datanew.json'
res = requests.get(url)

df_in = pd.DataFrame.from_dict(pd.json_normalize(res.json()), orient='columns')
df = df_in.drop(['sno', 'active', 'positive', 'cured', 'death', 'state_code'], axis = 1)

'''dropping unnecessary rows containing below words/characters'''
df['state_name'].replace('', np.nan, inplace = True)
df.dropna(subset =['state_name'], inplace = True)

'''adding date column with today's value'''
df['Date'] = datetime.date.today()

df.rename(columns={"new_positive": "Confirmed"}, inplace= True)
df.state_name[df.state_name == 'Telengana'] = 'Telangana'
# print(df)

csv_output_path = 'corona_database_extract_pythonanywhere.csv'
df.to_csv(csv_output_path, mode = 'a', header = False, index = False)
