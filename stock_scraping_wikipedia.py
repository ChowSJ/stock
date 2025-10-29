import requests as req
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup as bs
import lxml
import regex as re

# Website adress with stock info for NSE listed companies
url_to_scrape="https://en.wikipedia.org/wiki/List_of_companies_listed_on_the_National_Stock_Exchange_of_India"

# function to get requested webpage content

def request_to_webpage(url):
    response_from_server=req.get(url=url_to_scrape,headers={"User-Agent": "Mozilla/5.0"})
    if response_from_server.status_code != 200:
        print(f"The server responded with the {response_from_server.status_code} status code")
    else:
        soup=bs(response_from_server.content, 'lxml')
        return soup
    
# function to call header for the dataframe. Comapany and Symbol

def column_names(soup):
    bs_column=soup.find_all('th')
    column_header=[]
    for i in range(2):
        header_temp=bs_column[i].text.strip()
        column_header.append(header_temp)
    return column_header
    
# function to call sybols listed. 

def column_ticker_func(soup):
    elements = soup.css.select('div.mw-heading + table tr > td:nth-child(1) > a[href^="https://www.nseindia.com/get"]')
    return [element.text.strip() for element in elements]

# function to get the corresponding company name
def column_company_name_func(soup):
    elements = soup.css.select('div.mw-heading + table tr > td:nth-child(2)')
    return [element.text.strip() for element in elements]  # excluding the first two header rows
    

# calling the function request_to_webpage and getting the soup object
soup_output=request_to_webpage(url=url_to_scrape)

#calling the function column_names and getting the column names for the dataframe
column_name_output=column_names(soup=soup_output)  # column name output as colums of df

symbol_elements_output=column_ticker_func(soup=soup_output)  # list of symbols

company_elements_output=column_company_name_func(soup=soup_output)  # list of company names

data_lookup={column_name_output[0]:company_elements_output,
             column_name_output[1]:symbol_elements_output}

df_stocks_lookup=pd.DataFrame(data_lookup)
