from web_content_client import get_page_content

url =  'https://www.olx.com.br'
path = '/autos-e-pecas/carros-vans-e-utilitarios/flex/estado-rj'
page_number = 1

main_content = get_page_content(url=f'{ url }{ path }?o={page_number}')

links = [ link['href'] for link in main_content.find_all('a', attrs={ 'class': 'olx-ad-card__link-wrapper' }) ]

for link in links:
    ad_content = get_page_content(url=link)
    