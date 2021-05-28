import requests
from bs4 import BeautifulSoup
import pandas as pd


crypto_url = "https://finance.yahoo.com/cryptocurrencies"
r = requests.get(crypto_url)
data = r.text
soup = BeautifulSoup(data)

raw_data = {}
headers = []

for header_row in soup.find_all('thead'):
    for header in header_row.find_all('th'):
        headers.append(header.text)
        raw_data[header.text] = []

for rows in soup.find_all('tbody'):
    for row in rows.find_all('tr'):
        for idx, cell in enumerate(row.find_all('td')):
            header_value = headers[idx]
            raw_data[header_value].append(cell.text)
pd.DataFrame(raw_data)

#print(raw_data)
