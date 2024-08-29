import re
import math
from html import unescape
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from time import sleep

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
    code = url_content.find('span', attrs={'class', 'olx-text olx-text--caption olx-text--block olx-text--regular ad__sc-16iz3i7-0 kuirEE olx-color-neutral-120'})
    zipcode = perform_if_present(url_content.find('span', string='CEP'), lambda v : v.next_sibling) 
    city = perform_if_present(url_content.find('span', string='Município'), lambda v : v.next_sibling) 
    neighborhood = perform_if_present(url_content.find('span', string='Bairro'), lambda v : v.next_sibling) 
    creation_date = url_content.find('span', attrs={'class': 'olx-text olx-text--caption olx-text--block olx-text--regular ad__sc-1oq8jzc-0 eSgKoP olx-color-neutral-120'})
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
    price = perform_if_present(url_content.find('h2', attrs={'class', 'olx-text olx-text--title-large olx-text--block ad__sc-1leoitd-0 bpLbCi'}), lambda v : extract_price(v))
    #average_price = perform_if_present(url_content.find('span', attrs={'class': 'sc-gswNZR eIiKCz'}), lambda v : extract_price(v))
    #fipe_price = perform_if_present(url_content.find('span', attrs={'class': 'sc-gswNZR eIiKCz'}), lambda v : extract_price(v))
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
        #    'average_price': average_price,
        #    'fipe_price': fipe_price
        }
    }

def extract_float(text: str):
    if not text:
        return None
    extracted_price = re.search(r'(\d+).(\d+)', text)
    if extracted_price:
        return float(''.join(extracted_price.groups()))
    return None

def find_element_fallback(driver, paths):
    exception = None
    for path in paths:
        try:
            return driver.find_element(by='xpath', value=path).text
        except NoSuchElementException as e:
            exception = e
    raise exception

xpaths_average_price = [
    '//*[@id="content"]/div[2]/div/div[2]/div[1]/div[33]/div/div/div/div/div[1]/div/span',
    '//*[@id="content"]/div[2]/div/div[2]/div[1]/div[33]/div/div/div/div[2]/div[1]/div[1]/span',
    '//*[@id="content"]/div[2]/div/div[2]/div[1]/div[32]/div/div/div/div/div[1]/div/span',
    '//*[@id="content"]/div[2]/div/div[2]/div[1]/div[32]/div/div/div/div[2]/div[1]/div[1]/span',
    '//*[@id="content"]/div[2]/div/div[2]/div[1]/div[31]/div/div/div/div[2]/div[1]/div[1]/span',
    '//*[@id="content"]/div[2]/div/div[2]/div[1]/div[31]/div/div/div/div/div[1]/div[1]/span',
    '//*[@id="content"]/div[2]/div/div[2]/div[1]/div[31]/div/div/div/div/div[1]/div/span',
    ]
xpaths_fipe_price = [
    '//*[@id="content"]/div[2]/div/div[2]/div[1]/div[33]/div/div/div/div/div[2]/div/span',
    '//*[@id="content"]/div[2]/div/div[2]/div[1]/div[33]/div/div/div/div[2]/div[2]/div/span',
    '//*[@id="content"]/div[2]/div/div[2]/div[1]/div[32]/div/div/div/div/div[2]/div/span',
    '//*[@id="content"]/div[2]/div/div[2]/div[1]/div[32]/div/div/div/div[2]/div[2]/div/span',
    '//*[@id="content"]/div[2]/div/div[2]/div[1]/div[31]/div/div/div/div[2]/div[2]/div/span',
    '//*[@id="content"]/div[2]/div/div[2]/div[1]/div[31]/div/div/div/div/div[2]/div/span',
    ]

def get_average_price_and_fipe(url, wait=3):

    options = webdriver.ChromeOptions()
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-cache")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36")
    #options.add_argument('--proxy-server=%s' % proxy)
    #options.add_argument("--headless")
    #options.add_argument("--window-size=%s" % WINDOW_SIZE)
    options.add_experimental_option(
        "prefs", {
            # block image loading
            "profile.managed_default_content_settings.images": 2,
        }
    )

    driver = webdriver.Chrome(options=options)

    #driver.set_page_load_timeout(8)
    driver.get(url=url)
    sleep(wait)

    average_price = extract_float(find_element_fallback(driver=driver, paths=xpaths_average_price))
    fipe_price = extract_float(find_element_fallback(driver=driver, paths=xpaths_fipe_price))

    driver.delete_all_cookies()

    driver.close()
    driver.quit()

    return average_price, fipe_price

if __name__ == '__main__':
    print(get_average_price_and_fipe(url='https://rj.olx.com.br/rio-de-janeiro-e-regiao/autos-e-pecas/carros-vans-e-utilitarios/citroen-c3-picasso-exc-a-1303576958'))