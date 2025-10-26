import pandas as pd
import requests as rq
from bs4 import BeautifulSoup as bs
import lxml
import numpy as np

request_url = "https://en.wikipedia.org/wiki/List_of_national_parks_of_India"

national_park_wiki=rq.get(request_url, headers={"User-Agent": "Mozilla/5.0"})

soup=bs(national_park_wiki.content, 'lxml')

soup_table_body=soup.find_all('tbody')

soup_table_struct=soup_table_body[0]

soup_table_body=soup_table_struct.find_all('tr')


state_list_all=[]

for item in soup_table_body:
    stat_list_temp=item.text.strip().split('\n')
    state_list_all.append(stat_list_temp)

df_national_park=pd.DataFrame(state_list_all)

df_national_park.dropna(axis=1, how='all', inplace=True)

df_national_park.replace("",np.nan, inplace=True)

df_national_park.dropna(axis=1,how='all',inplace=True)

columns_names=df_national_park.iloc[0].values.tolist()

df_national_park.columns=columns_names

df_national_park.drop(index=0, inplace=True)
