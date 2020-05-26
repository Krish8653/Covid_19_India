import pandas as pd
import requests
import datetime
import pyodbc
# from bs4 import BeautifulSoup
# from tabulate import tabulate

url = 'https://www.mohfw.gov.in/'
html = requests.get(url).content
df_list = pd.read_html(html)
df = df_list[-1]
#print(df.head())
df = df.drop(['S. No.'], axis = 1)
df.columns = ["State", "Total_Confirmed", "Total_Cured", "Total_Death"]
df = df[df.State != "Total#"]
# search_for = ['more','States','Including','figures','Cases','State']
search_for = ['\*','\#','Cases','State']
df = df[~df.State.str.contains('|'.join(search_for))]
df['Date'] = datetime.date.today()
#df.to_csv('my data.csv', index = False)
#print(df)

sql_conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; SERVER=.; DATABASE=TEST;   Trusted_Connection=yes')
cursor = sql_conn.cursor()
query = "INSERT INTO COVID ([State],[Total_Confirmed],[Total_Cured],[Total_Death],[Date]) VALUES (?,?,?,?,?);"

for index,rows in df.iterrows():
    values = (rows[0],rows[1],rows[2],rows[3],rows[4])
    print(values)
    cursor.execute(query, values)
    sql_conn.commit()
cursor.close()
sql_conn.close()

print(df.shape)