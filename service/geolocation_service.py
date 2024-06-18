from retry import retry
import logging
from client.geolocation_client import get_geocode
import traceback

log = logging.getLogger(__name__)

@retry(exceptions=(TypeError), tries=3, delay=2, logger=log)
def resolve_geolocation(adv):
    if not adv.zipcode:
        log.warn(f'Not processing! Zipcode is null!')
        return
    if not adv.lat or not adv.lon:
        log.info(f'*** FINDING LOCATION')
        try:
            geocode = get_geocode(adv.zipcode)
            if geocode:
                adv.lat = geocode[0]
                adv.lon = geocode[1]
        except TypeError as e:
            log.error(f'Error finding location (retrying!) [ link: { adv.url } - { traceback.format_exc() }')
            raise e
        except Exception as e:
            log.error(f'Error finding location [ link: { adv.url } - { traceback.format_exc() }')
