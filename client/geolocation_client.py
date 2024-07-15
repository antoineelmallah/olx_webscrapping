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
        retry = 0
        result = None
        while result is None and retry <= 4:
            if retry < 4 and zipcode[7 - retry] == '0':
                retry = retry + 1
                continue
            z = zipcode[:(8 - retry)] + ('0' * retry)
            result = get_with_zipcodestack(zipcode=z)
            retry = retry + 1
        return result

if __name__ == '__main__':
    print(get_geocode('21700100'))