import brazilcep
from geopy.geocoders import Nominatim
import requests
import os

def get_with_brazilcep(zipcode):
    address = brazilcep.get_address_from_cep(zipcode)
    geolocator = Nominatim(user_agent='test_app')
    text = f'{ address["street"] }, { address["city"] }, { address["district"] }'
    location = geolocator.geocode(text).raw
    return float(location['lat']), float(location['lon'])

def get_with_zipcodestack(zipcode):
    url = 'https://api.zipcodestack.com/v1/search'
    params = {
        'codes': zipcode,
        'country': 'br',
    }
    headers = { 'apikey': os.environ['ZIPCODESTACK_API_KEY'] }
    try:
        response = requests.request('GET', url, headers=headers, params=params)
        if not response:
            return None
        latlong = response.json()['results'][zipcode][0]
        return (float(latlong['latitude']), float(latlong['longitude']))
    except Exception as e:
        return None


def get_geocode(zipcode):
    try:
        return get_with_brazilcep(zipcode)
    except Exception as e:
        result = get_with_zipcodestack(zipcode)
        return result if result else get_with_zipcodestack(zipcode[:5] + '000')

if __name__ == '__main__':
    print(get_geocode('25655151'))