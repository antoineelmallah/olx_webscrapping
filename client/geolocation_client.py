import brazilcep
from geopy.geocoders import Nominatim

def get_geocode(zipcode):
    try:
        address = brazilcep.get_address_from_cep(zipcode)
        geolocator = Nominatim(user_agent='test_app')
        text = f'{ address["street"] }, { address["city"] }, { address["district"] }'
        location = geolocator.geocode(text).raw
        return float(location['lat']), float(location['lon'])
    except Exception as e:
        return None

if __name__ == '__main__':
    print(get_geocode('25655151'))