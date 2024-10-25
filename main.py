from client.web_content_client import get_page_content
from utils.content_extractor import get_total_pages
from mapper import page_content_to_advertising_entity
from persistence.repository import persist_advertisement
import logging
import traceback
from datetime import datetime
from tqdm import tqdm
from service.price_service import resolve_prices
from service.geolocation_service import resolve_geolocation

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, filename=f'./logs/log_{ datetime.now().isoformat(sep="_") }.log')

def before_persist(adv):
    try:
        resolve_geolocation(adv=adv)
        resolve_prices(adv=adv)
    except Exception as e:
        log.error(f'Error on before save [ link: { adv.url } - { traceback.format_exc() }')
        

def process_link(link, count, page, pages):
    log.info(f'[{ count }/{ page }/{ pages }] Processing link { link }')
    try:
        ad_content = get_page_content(url=link)
        advertising_entity = page_content_to_advertising_entity(ad_content, link)
        persist_advertisement(advertising_entity, before_persist=before_persist)
    except Exception as e:
        log.error(f'Error NOT PROCESSING!! [{ count }/{ page }/{ pages }] link: { link } - { traceback.format_exc() }')

def process_main_page(main_content, page, pages):
    count = 0
    links = [ link['href'] for link in main_content.find_all('a', attrs={ 'class': 'olx-ad-card__link-wrapper' }) ]
    for link in links:
        count = count + 1
        try:
            process_link(link=link, count=count, page=page, pages=pages)
        except:
            pass

def main():
    url =  'https://www.olx.com.br'
    path = '/autos-e-pecas/carros-vans-e-utilitarios/estado-rj?ps=30000&pe=50000&lis=home_body_search_bar_2020'

    main_content = get_page_content(url=f'{ url }{ path }&o=1')

    pages = get_total_pages(main_content)

    pbar = tqdm(range(1, pages))
    for page in pbar:
        process_main_page(main_content, page, pages)
        main_content = get_page_content(url=f'{ url }{ path }&o={ page + 1 }')
        if page + 1 == pages:
            process_main_page(main_content, page, pages)

#import cProfile
#cProfile.run('main()')

main()
