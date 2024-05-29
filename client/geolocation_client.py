import brazilcep
from geopy.geocoders import Nominatim
import requests
import os

def get_geocode(zipcode):
    try:
        address = brazilcep.get_address_from_cep(zipcode)
        geolocator = Nominatim(user_agent='test_app')
        text = f'{ address["street"] }, { address["city"] }, { address["district"] }'
        location = geolocator.geocode(text).raw
        return float(location['lat']), float(location['lon'])
    except Exception as e:
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

if __name__ == '__main__':
    print(get_geocode('25655151'))