from client.web_content_client import get_page_content
from utils.content_extractor import get_total_pages
from mapper import page_content_to_advertising_entity
from persistence.repository import persist_advertisement
import logging

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

url =  'https://www.olx.com.br'
path = '/autos-e-pecas/carros-vans-e-utilitarios/flex/estado-rj'

main_content = get_page_content(url=f'{ url }{ path }?o=1')

pages = get_total_pages(main_content)

logging.info(f'==> Processing page 1/{ pages }')

for page in range(2, pages):
    logging.info(f'==> Processing page { page }/{ pages }')
    links = [ link['href'] for link in main_content.find_all('a', attrs={ 'class': 'olx-ad-card__link-wrapper' }) ]
    for link in links:
        logging.info(' ** Processing link { link }')
        ad_content = get_page_content(url=link)
        advertising_entity = page_content_to_advertising_entity(ad_content, link)
        persist_advertisement(advertising_entity)

    main_content = get_page_content(url=f'{ url }{ path }?o={ page + 1 }')
    