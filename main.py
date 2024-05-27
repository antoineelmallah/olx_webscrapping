from client.web_content_client import get_page_content
from utils.content_extractor import get_total_pages
from mapper import page_content_to_advertising_entity
from persistence.repository import persist_advertisement
import logging
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
        logging.info(f'[{ count }/{ page }/{ pages }] Processing link { link }')
        ad_content = get_page_content(url=link)
        advertising_entity = page_content_to_advertising_entity(ad_content, link)
        try:
            persist_advertisement(advertising_entity)
        except Exception as e:
            log.error(f'Error [{ count }/{ page }/{ pages }]', e)

def main():

    url =  'https://www.olx.com.br'
    path = '/autos-e-pecas/carros-vans-e-utilitarios/flex/estado-rj'

    main_content = get_page_content(url=f'{ url }{ path }?o=1')

    pages = get_total_pages(main_content)

    pbar = tqdm(range(1, pages))
    for page in pbar:
        process_page(main_content, page, pages)
        main_content = get_page_content(url=f'{ url }{ path }?o={ page + 1 }')

#import cProfile
#cProfile.run('main()')

main()
