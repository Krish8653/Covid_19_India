import pandas as pd
import requests
import datetime
import pyodbc
from openpyxl import load_workbook
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

sql_conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; SERVER=.; DATABASE=COVID_19;   Trusted_Connection=yes')
cursor = sql_conn.cursor()
query = "INSERT INTO [dbo].[MOHFW] ([State],[Total_Confirmed],[Total_Cured],[Total_Death],[Date]) VALUES (?,?,?,?,?);"

for index,rows in df.iterrows():
    values = (rows[0],rows[1],rows[2],rows[3],rows[4])
    #print(values)
    cursor.execute(query, values)
    sql_conn.commit()

'''UPDATING THE Corona_database_extract.xlsx file'''
select_query = "Select [State],[Total_Confirmed],[Total_Cured],[Total_Death],FORMAT([Date],'dd-MM-yyyy') AS DATE,[Confirmed_cases_on_this_day],[Recovered_cases_on_this_day],[Death_cases_on_this_day] from [dbo].[MOHFW]  where [Date] = CAST(Getdate() AS DATE);"
select_df = pd.read_sql(select_query, sql_conn)
book = load_workbook("D:\\Projects\\Covid_19_India\\Corona_database_extract.xlsx")
writer = pd.ExcelWriter('D:\\Projects\\Covid_19_India\\Corona_database_extract.xlsx', engine= 'openpyxl') # pylint: disable=abstract-class-instantiated
writer.book = book
writer.sheets = dict((ws.title, ws) for ws in book.worksheets)

reader = pd.read_excel(open("D:\\Projects\\Covid_19_India\\Corona_database_extract.xlsx",'rb'),sheet_name= 'Latest Data')
select_df.to_excel(writer,sheet_name= 'Latest Data' ,index=False,header=False,startrow=len(reader)+1)

writer.save()
writer.close()

cursor.close()
sql_conn.close()


