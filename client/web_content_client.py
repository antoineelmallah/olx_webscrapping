from bs4 import BeautifulSoup
import cloudscraper

def get_page_content(url: str):
    scraper = cloudscraper.create_scraper()
    content = scraper.get(url=url).text
    return BeautifulSoup(content, features="html.parser")