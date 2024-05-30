import sys
sys.path.insert(1, '/home/mallah/Documents/olx_webscrapping/')
from persistence.repository import find_advertisements_without_geocode, persist
from client.geolocation_client import get_geocode
from tqdm import tqdm

advertisements = find_advertisements_without_geocode()

pbar = tqdm(range(len(advertisements)))
for idx in pbar:
    adv = advertisements[idx]
    if adv.zipcode:
        latlong = get_geocode(adv.zipcode)
        if latlong:
            adv.lat = latlong[0]
            adv.lon = latlong[1]
            persist(adv)
