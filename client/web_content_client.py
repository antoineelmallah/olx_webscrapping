from bs4 import BeautifulSoup
from curl_cffi import requests

def get_page_content(url: str):
    content = requests.get(url=url, impersonate='chrome110').text
    return BeautifulSoup(content, features="html.parser")