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
    return math.ceil(total_size / page_size)

def get_value(element):
    if not element:
        return None
    return unescape(element.text)

def perform_if_present(value, function, result = None):
    if value:
        if function:
            return function(value)
        return value
    return result

def extract_price(text):
    pattern = r'R\S (\d+)\.(\d+)'
    if text and text.text:
        matchs = re.search(pattern, text.text)
        if matchs:
            return int(''.join(matchs.groups()))
    return None

def extract_doors(text):
    pattern = r'(\d) portas'
    if text and text.text:
        matchs = re.search(pattern, text.text)
        if matchs:
            return int(matchs.group(1))
    return None


def read_content(url_content):
    code = url_content.find('span', attrs={'class', 'olx-text olx-text--caption olx-text--block olx-text--regular ad__sc-16iz3i7-0 hjLLUR olx-color-neutral-120'})
    zipcode = perform_if_present(url_content.find('span', string='CEP'), lambda v : v.next_sibling) 
    city = perform_if_present(url_content.find('span', string='Município'), lambda v : v.next_sibling) 
    neighborhood = perform_if_present(url_content.find('span', string='Bairro'), lambda v : v.next_sibling) 
    creation_date = url_content.find('span', attrs={'class': 'olx-text olx-text--caption olx-text--block olx-text--regular ad__sc-1oq8jzc-0 dWayMW olx-color-neutral-120'})
    description = url_content.find('h1')
    hp = perform_if_present(url_content.find('span', string='Potência do motor'), lambda v : v.next_sibling) 
    gnv = perform_if_present(url_content.find('span', string='Possui Kit GNV'), lambda v : v.next_sibling)
    year = perform_if_present(url_content.find('span', string='Ano'), lambda v : v.next_sibling)
    mileage = perform_if_present(url_content.find('span', string='Quilometragem'), lambda v : v.next_sibling)
    doors = perform_if_present(url_content.find('span', string='Portas'), lambda v : extract_doors(v.next_sibling))
    category = perform_if_present(url_content.find('span', string='Categoria'), lambda v : v.next_sibling)
    model = perform_if_present(url_content.find('span', string='Modelo'), lambda v : v.next_sibling)
    brand = perform_if_present(url_content.find('span', string='Marca'), lambda v : v.next_sibling)
    vehicle_type = perform_if_present(url_content.find('span', string='Tipo de veículo'), lambda v : v.next_sibling)
    fuel = perform_if_present(url_content.find('span', string='Combustível'), lambda v : v.next_sibling)
    gear = perform_if_present(url_content.find('span', string='Câmbio'), lambda v : v.next_sibling)
    color = perform_if_present(url_content.find('span', string='Cor'), lambda v : v.next_sibling)
    steering = perform_if_present(url_content.find('span', string='Tipo de direção'), lambda v : v.next_sibling)
    price = perform_if_present(url_content.find('h2', attrs={'class', 'olx-text olx-text--title-large olx-text--block ad__sc-1leoitd-0 bJHaGt'}), lambda v : extract_price(v))
    average_price = perform_if_present(url_content.find('span', attrs={'class': 'sc-gswNZR eIiKCz'}), lambda v : extract_price(v))
    fipe_price = perform_if_present(url_content.find('span', attrs={'class': 'sc-gswNZR eIiKCz'}), lambda v : extract_price(v))
    accessories = [ s.text for s in perform_if_present(url_content.find('span', string='Opcionais'), lambda v : v.next_sibling.extract(), result=[]) ]

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
            'doors': doors,
            'category': get_value(category),
            'model': get_value(model),
            'brand': get_value(brand),
            'vehicle_type': get_value(vehicle_type),
            'fuel': get_value(fuel),
            'gear': get_value(gear),
            'color': get_value(color),
            'steering': get_value(steering),
            'accessories': accessories,
        },
        'state': {
            'price': price,
            'average_price': average_price,
            'fipe_price': fipe_price
        }
    }

if __name__ == '__main__':
    import sys
    sys.path.insert(0, '/home/mallah/Documents/olx_webscrapping')
    from client.web_content_client import get_page_content
    url = 'http://localhost:3000/template'
    print(read_content(get_page_content(url)))