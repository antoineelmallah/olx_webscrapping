from client.web_content_client import get_page_content
from utils.regex_utils import get_total_pages

url =  'https://www.olx.com.br'
path = '/autos-e-pecas/carros-vans-e-utilitarios/flex/estado-rj'

main_content = get_page_content(url=f'{ url }{ path }?o={1}')

pages = get_total_pages(main_content)

for page in range(1, pages + 1):
    links = [ link['href'] for link in main_content.find_all('a', attrs={ 'class': 'olx-ad-card__link-wrapper' }) ]
    for link in links:
        ad_content = get_page_content(url=link)

    main_content = get_page_content(url=f'{ url }{ path }?o={ page + 1 }')
    