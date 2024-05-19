from bs4 import BeautifulSoup
from persistence.model import Advertisement, Vehicle, InstantState
from utils.content_extractor import read_content
import utils.formatter as formatter

def page_content_to_vehicle_entity(advertisement: Advertisement, dto) -> Vehicle:
    
    dto_vehicle = dto['vehicle']
    
    result = Vehicle()
    result.description = formatter.get_as_type(dto_vehicle['description'], str)
    result.hp = formatter.get_as_type(dto_vehicle['hp'], float)
    result.gnv = formatter.get_gnv(dto_vehicle['gnv'])
    result.year = formatter.get_as_type(dto_vehicle['year'], int)
    result.mileage = formatter.get_as_type(dto_vehicle['mileage'], float)
    result.doors = formatter.get_as_type(dto_vehicle['doors'], int)

    result.advertisement = advertisement

    result.category = dto_vehicle['category']
    result.model = dto_vehicle['model']
    result.brand = dto_vehicle['brand']
    result.fuel = dto_vehicle['fuel']
    result.gear = dto_vehicle['gear']
    result.color = dto_vehicle['color']
    result.steering = dto_vehicle['steering']

    return result

def page_content_to_instant_state_entity(advertisement: Advertisement, dto) -> InstantState:

    dto_state = dto['state']
    
    result = InstantState()
    result.price = formatter.get_as_type(dto_state['price'], float)
    result.average_price = formatter.get_as_type(dto_state['average_price'], float)
    result.fipe_price = formatter.get_as_type(dto_state['fipe_price'], float)

    return result

def page_content_to_advertising_entity(content: BeautifulSoup, url: str) -> Advertisement:

    dto = read_content(content)
    
    result = Advertisement()
    result.code = formatter.get_code(dto['code'])
    result.zipcode = formatter.get_as_type(dto['zipcode'], str)
    result.city = formatter.get_as_type(dto['city'], str)
    result.neighborhood = formatter.get_as_type(dto['neighborhood'], str)
    result.creation_date = formatter.get_creation_datetime(dto['creation_date'])
    result.url = url
    result.vehicle = page_content_to_vehicle_entity(result, dto)
    result.states.append(page_content_to_instant_state_entity(result, dto))

    return result

from client.web_content_client import get_page_content

url = 'http://localhost:3000/template'

print(page_content_to_advertising_entity(get_page_content(url), url))