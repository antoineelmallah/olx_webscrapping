import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import re
import time
from datetime import datetime

### scrapping
import requests
from urllib.request import urlopen
from bs4 import BeautifulSoup

from web_content_client import get_page_content

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0',
    'Accept-Encodding': 'gzip, defalte',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'DNT': '1',
    'Connection': 'close',
    'Upgrade-Insegure-Requests': '1'
}

url =  'https://www.olx.com.br'
path = '/autos-e-pecas/carros-vans-e-utilitarios/flex/estado-rj'
page_number = 1

main_content = get_page_content(url=f'{ url }{ path }?o={page_number}')

links = [ link['href'] for link in main_content.find_all('a', attrs={ 'class': 'olx-ad-card__link-wrapper' }) ]

for link in links:
    ad_content = get_page_content(url=link)
    