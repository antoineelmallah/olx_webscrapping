import re
import math
from html import unescape

def get_total_pages(main_content):
    pattern = r'(\d+) - (\d+) de ([0-9\.]+) resultados'
    matchs = [ re.search(pattern, p.text) for p in main_content.find_all('p') if re.search(pattern, p.text) ]
    if not len(matchs):
        return 0
    match = matchs[0]
    page_size = int(match.group(2))
    total_size = int(re.sub(r'\.', '', match.group(3)))
    print(page_size, '/', total_size)
    return math.ceil(total_size / page_size)

def get_value(element):
    if not element:
        return None
    return unescape(element.text)

def read_content(url_content):
    code = url_content.find('span', attrs={'class', 'olx-text olx-text--caption olx-text--block olx-text--regular ad__sc-16iz3i7-0 hjLLUR olx-color-neutral-120'})
    zipcode = url_content.find('span', string='CEP').next_sibling
    city = url_content.find('span', string='Município').next_sibling
    neighborhood = url_content.find('span', string='Bairro').next_sibling
    creation_date = url_content.find('span', attrs={'class': 'olx-text olx-text--caption olx-text--block olx-text--regular ad__sc-1oq8jzc-0 dWayMW olx-color-neutral-120'})
    description = url_content.find('h1')
    hp = url_content.find('span', string='Potência do motor').next_sibling
    gnv = url_content.find('span', string='Possui Kit GNV').next_sibling
    year = url_content.find('span', string='Ano').next_sibling
    mileage = url_content.find('span', string='Quilometragem').next_sibling
    doors = url_content.find('span', string='Portas').next_sibling
    category = url_content.find('span', string='Categoria').next_sibling
    model = url_content.find('span', string='Modelo').next_sibling
    brand = url_content.find('span', string='Marca').next_sibling
    vehicle_type = url_content.find('span', string='Tipo de veículo').next_sibling
    fuel = url_content.find('span', string='Combustível').next_sibling
    gear = url_content.find('span', string='Câmbio').next_sibling
    color = url_content.find('span', string='Cor').next_sibling
    steering = url_content.find('span', string='Tipo de direção').next_sibling
    price = url_content.find('h2', attrs={'class', 'olx-text olx-text--title-large olx-text--block ad__sc-1leoitd-0 bJHaGt'})
    average_price = url_content.find('span', attrs={'class': 'sc-gswNZR eIiKCz'})
    fipe_price = url_content.find('span', attrs={'class': 'sc-gswNZR eIiKCz'})

    return {
        'code': get_value(code),
        'zipcode': get_value(zipcode),
        'city': get_value(city),
        'neighborhood': get_value(neighborhood),
        'creation_date': get_value(creation_date),
        'vehicle': {
            'description': get_value(description),
            'hp': get_value(hp),
            'gnv': get_value(gnv),
            'year': get_value(year),
            'mileage': get_value(mileage),
            'doors': get_value(doors),
            'category': get_value(category),
            'model': get_value(model),
            'brand': get_value(brand),
            'vehicle_type': get_value(vehicle_type),
            'fuel': get_value(fuel),
            'gear': get_value(gear),
            'color': get_value(color),
            'steering': get_value(steering),
        },
        'state': {
            'price': get_value(price),
            'average_price': get_value(average_price),
            'fipe_price': get_value(fipe_price)
        }
    }

#import sys
#sys.path.insert(0, '/home/mallah/Documents/olx_webscrapping')
#from client.web_content_client import get_page_content
#url = 'http://localhost:3000/template'
#print(read_content(get_page_content(url)))