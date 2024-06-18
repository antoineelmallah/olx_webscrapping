import sys
sys.path.insert(1, '/home/mallah/Documents/olx_webscrapping/')
from persistence.repository import find_advertisements_without_prices, persist
from tqdm import tqdm
from service.price_service import resolve_prices

advertisements = find_advertisements_without_prices()

pbar = tqdm(range(len(advertisements)))
for idx in pbar:
    adv = advertisements[idx]
    try:
        resolve_prices(adv=adv)
        vehicle = adv.vehicle
        if vehicle.average_price or vehicle.fipe_price:
            persist(adv)
    except Exception as e:
        pass