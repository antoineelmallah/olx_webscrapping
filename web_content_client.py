import requests
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0',
    'Accept-Encodding': 'gzip, defalte',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'DNT': '1',
    'Connection': 'close',
    'Upgrade-Insegure-Requests': '1'
}

def get_page_content(url: str):
    r = requests.get(url=url, headers=headers)
    content = r.content
    return BeautifulSoup(content)