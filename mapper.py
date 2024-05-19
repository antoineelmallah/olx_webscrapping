from bs4 import BeautifulSoup
from persistence.model import Advertisement, Vehicle, InstantState
from utils.content_extractor import read_content

def page_content_to_vehicle_entity(content: BeautifulSoup, advertisement: Advertisement, dto) -> Vehicle:
    
    dto_vehicle = dto['vehicle']
    
    result = Vehicle()
    result.description = dto_vehicle['description']
    result.hp = dto_vehicle['hp']
    result.gnv = dto_vehicle['gnv']
    result.year = dto_vehicle['year']
    result.mileage = dto_vehicle['mileage']
    result.doors = dto_vehicle['doors']

    result.advertisement = advertisement

    result.category = dto_vehicle['category']
    result.model = dto_vehicle['model']
    result.brand = dto_vehicle['brand']
    result.fuel = dto_vehicle['fuel']
    result.gear = dto_vehicle['gear']
    result.color = dto_vehicle['color']
    result.steering = dto_vehicle['steering']

    return result

def page_content_to_instant_state_entity(content: BeautifulSoup, advertisement: Advertisement, dto) -> InstantState:

    dto_state = dto['state']
    
    result = InstantState()
    result.price = dto_state['price']
    result.average_price = dto_state['average_price']
    result.fipe_price = dto_state['fipe_price']

    return result

def page_content_to_advertising_entity(content: BeautifulSoup, url: str) -> Advertisement:

    dto = read_content(content)
    
    result = Advertisement()
    result.code = dto['code']
    result.zipcode = dto['zipcode']
    result.city = dto['city']
    result.neighborhood = dto['neighborhood']
    result.creation_date = dto['creation_date']
    result.url = url
    result.vehicle = page_content_to_vehicle_entity(content, result, dto)
    result.states.append(page_content_to_instant_state_entity(content, result, dto))

    return result

    