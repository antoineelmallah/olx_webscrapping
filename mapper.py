from bs4 import BeautifulSoup
import persistence.model as model
from utils.content_extractor import read_content
import utils.formatter as formatter

def page_content_to_domain(description, domain_class):
    if not description:
        return None
    if len(description.strip()) == 0:
        return None
    result = domain_class()
    result.description = description
    return result

def page_content_to_vehicle_entity(advertisement: model.Advertisement, dto) -> model.Vehicle:
    
    dto_vehicle = dto['vehicle']
    
    result = model.Vehicle()
    result.description = formatter.get_as_type(dto_vehicle['description'], str)
    result.hp = formatter.get_as_type(dto_vehicle['hp'], float)
    result.gnv = formatter.get_gnv(dto_vehicle['gnv'])
    result.year = formatter.get_as_type(dto_vehicle['year'], int)
    result.mileage = formatter.get_as_type(dto_vehicle['mileage'], float)
    result.doors = formatter.get_as_type(dto_vehicle['doors'], int)

    result.advertisement = advertisement

    result.category = page_content_to_domain(dto_vehicle['category'], model.Category)
    result.model = page_content_to_domain(dto_vehicle['model'], model.Model)
    result.brand = page_content_to_domain(dto_vehicle['brand'], model.Brand)
    result.vehicle_type = page_content_to_domain(dto_vehicle['vehicle_type'], model.VehicleType)
    result.fuel = page_content_to_domain(dto_vehicle['fuel'], model.Fuel)
    result.gear = page_content_to_domain(dto_vehicle['gear'], model.Gear)
    result.color = page_content_to_domain(dto_vehicle['color'], model.Color)
    result.steering = page_content_to_domain(dto_vehicle['steering'], model.Steering)

    return result

def page_content_to_instant_state_entity(advertisement: model.Advertisement, dto) -> model.InstantState:

    dto_state = dto['state']
    
    result = model.InstantState()
    result.price = formatter.get_as_type(dto_state['price'], float)
    result.average_price = formatter.get_as_type(dto_state['average_price'], float)
    result.fipe_price = formatter.get_as_type(dto_state['fipe_price'], float)

    return result

def page_content_to_advertising_entity(content: BeautifulSoup, url: str) -> model.Advertisement:

    dto = read_content(content)
    
    result = model.Advertisement()
    result.code = formatter.get_code(dto['code'])
    result.zipcode = formatter.get_as_type(dto['zipcode'], str)
    result.city = formatter.get_as_type(dto['city'], str)
    result.neighborhood = formatter.get_as_type(dto['neighborhood'], str)
    result.creation_date = formatter.get_creation_datetime(dto['creation_date'])
    result.url = url
    result.vehicle = page_content_to_vehicle_entity(result, dto)
    result.states.append(page_content_to_instant_state_entity(result, dto))

    return result
