import requests, json
import numpy as np
import pandas as pd
from pandas.io.json import json_normalize
# from datetime import timedelta
import datetime
import pyodbc
from openpyxl import load_workbook

url = 'https://www.mohfw.gov.in/data/datanew.json'
res = requests.get(url)

with open("data.json", "w") as f:
    json.dump(res.json(), f)

with open("data.json") as f:
    data = json.load(f)
df_in = pd.DataFrame.from_dict(pd.json_normalize(data), orient='columns')


df = df_in.drop(['sno', 'active', 'positive', 'cured', 'death', 'state_code'], axis = 1)

'''dropping unnecessary rows containing below words/characters'''
df['state_name'].replace('', np.nan, inplace = True)
df.dropna(subset =['state_name'], inplace = True)

'''adding date column with value today'''
df['Date'] = datetime.date.today()

# print(df)

df.rename(columns={"new_positive": "Confirmed"}, inplace= True)
df.state_name[df.state_name == 'Telengana'] = 'Telangana'
# print(df)

'''creatimg connection to local sql server DATABASE'''
sql_conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; SERVER=.; DATABASE=COVID_19;   Trusted_Connection=yes')
cursor = sql_conn.cursor()
query = "INSERT INTO [dbo].[MOHFW] ([State],[Total_Confirmed],[Total_Cured],[Total_Death],[Date],[Total_Active]) VALUES (?,?,?,?,?,?);"

'''loading data into sql db'''
for index,rows in df.iterrows():
    values = (rows[0],rows[2],rows[3],rows[4],rows[5],rows[1])
    #print(values)
    cursor.execute(query, values)
    sql_conn.commit()

'''UPDATING THE Corona_database_extract.xlsx file'''
select_query = "Select [State],[Total_Confirmed],[Total_Cured],[Total_Death],FORMAT([Date],'dd-MM-yyyy') AS DATE,[Total_confirmed],[Confirmed_cases_on_this_day],[Recovered_cases_on_this_day],[Death_cases_on_this_day] from [dbo].[MOHFW]  where [Date] = CAST(Getdate() AS DATE);"
select_df = pd.read_sql(select_query, sql_conn)
book = load_workbook("D:\\Projects\\Covid_19_India\\Corona_database_extract.xlsx")
writer = pd.ExcelWriter('D:\\Projects\\Covid_19_India\\Corona_database_extract.xlsx', engine= 'openpyxl') # pylint: disable=abstract-class-instantiated
writer.book = book
writer.sheets = dict((ws.title, ws) for ws in book.worksheets)

'''reading the existing data to append new data from the last+1 line'''
reader = pd.read_excel(open("D:\\Projects\\Covid_19_India\\Corona_database_extract.xlsx",'rb'),sheet_name= 'Latest Data')
select_df.to_excel(writer,sheet_name= 'Latest Data' ,index=False,header=False,startrow=len(reader)+1)

writer.save()
writer.close()

cursor.close()
sql_conn.close()