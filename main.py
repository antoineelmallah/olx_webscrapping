from client.web_content_client import get_page_content
from utils.content_extractor import get_total_pages
from mapper import page_content_to_advertising_entity
from persistence.repository import persist_advertisement
import logging
import traceback
from retry import retry
from datetime import datetime
from tqdm import tqdm

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, filename=f'./logs/log_{ datetime.now().isoformat(sep="_") }.log')

@retry(Exception, tries=3, delay=2, logger=log)
def process_page(main_content, page, pages):
    count = 0
    links = [ link['href'] for link in main_content.find_all('a', attrs={ 'class': 'olx-ad-card__link-wrapper' }) ]
    for link in links:
        count = count + 1
        log.info(f'[{ count }/{ page }/{ pages }] Processing link { link }')
        try:
            ad_content = get_page_content(url=link)
            advertising_entity = page_content_to_advertising_entity(ad_content, link)
            persist_advertisement(advertising_entity)
        except Exception as e:
            log.error(f'Error [{ count }/{ page }/{ pages }] link: { link } - { traceback.format_exc() }')

def main():
    url =  'https://www.olx.com.br'
    path = '/autos-e-pecas/carros-vans-e-utilitarios/estado-rj?ctp=9&ctp=8&ctp=5&ctp=3&ctp=7&f=p&gb=1&gb=2&gb=3&me=100000&ms=0&pe=50000&ps=30000&re=75&rs=50&fncs=1'

    main_content = get_page_content(url=f'{ url }{ path }&o=1')

    pages = get_total_pages(main_content)

    pbar = tqdm(range(1, pages))
    for page in pbar:
        process_page(main_content, page, pages)
        main_content = get_page_content(url=f'{ url }{ path }&o={ page + 1 }')

#import cProfile
#cProfile.run('main()')

main()
