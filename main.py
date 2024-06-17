from client.web_content_client import get_page_content
from utils.content_extractor import get_total_pages
from mapper import page_content_to_advertising_entity
from persistence.repository import persist_advertisement
import logging
import traceback
from retry import retry
from datetime import datetime
from tqdm import tqdm
from client.geolocation_client import get_geocode
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from utils.content_extractor import get_average_price_and_fipe

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, filename=f'./logs/log_{ datetime.now().isoformat(sep="_") }.log')

@retry(exceptions=(TypeError), tries=3, delay=2, logger=log)
def resolve_geolocation(adv):
    if not adv.zipcode:
        log.warn(f'Not processing! Zipcode is null!')
        return
    if not adv.lat or not adv.lon:
        log.info(f'*** FINDING LOCATION')
        try:
            geocode = get_geocode(adv.zipcode)
            if geocode:
                adv.lat = geocode[0]
                adv.lon = geocode[1]
        except TypeError as e:
            log.error(f'Error finding location (retrying!) [ link: { adv.url } - { traceback.format_exc() }')
            raise e
        except Exception as e:
            log.error(f'Error finding location [ link: { adv.url } - { traceback.format_exc() }')


@retry(exceptions=(TimeoutException, NoSuchElementException), tries=3, delay=2, logger=log)
def resolve_prices(adv):
    vehicle = adv.vehicle
    if not vehicle:
        return
    if not vehicle.average_price or not vehicle.fipe_price:
        log.info(f'*** FINDING PRICES')
        try:
            average_price, fipe_price = get_average_price_and_fipe(url=adv.url)
            vehicle.average_price = average_price
            vehicle.fipe_price = fipe_price
        except (TimeoutException, NoSuchElementException) as e:
            log.error(f'Error finding prices (retrying!) [ link: { adv.url } - { traceback.format_exc() }')
            raise e
        except Exception as e:
            log.error(f'Error finding prices [ link: { adv.url } - { traceback.format_exc() }')


def before_persist(adv):
    try:
        #resolve_geolocation(adv=adv)
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
    path = '/autos-e-pecas/carros-vans-e-utilitarios/estado-rj?ctp=9&ctp=8&ctp=5&ctp=3&ctp=7&f=p&gb=1&gb=2&gb=3&me=100000&ms=0&pe=50000&ps=30000&re=75&rs=50&fncs=1'

    main_content = get_page_content(url=f'{ url }{ path }&o=1')

    pages = get_total_pages(main_content)

    pbar = tqdm(range(1, pages))
    for page in pbar:
        process_main_page(main_content, page, pages)
        main_content = get_page_content(url=f'{ url }{ path }&o={ page + 1 }')

#import cProfile
#cProfile.run('main()')

main()
