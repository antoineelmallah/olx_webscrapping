from retry import retry
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from utils.content_extractor import get_average_price_and_fipe
import logging
from datetime import datetime
import traceback

log = logging.getLogger(__name__)

@retry(exceptions=(TimeoutException, NoSuchElementException), tries=3, delay=2, logger=log)
def resolve_prices(adv):
    vehicle = adv.vehicle
    if not vehicle:
        return
    if not vehicle.average_price or not vehicle.fipe_price:
        log.info(f'*** FINDING PRICES')
        try:
            average_price, fipe_price = get_average_price_and_fipe(url=adv.url)
            vehicle.average_price = average_price
            vehicle.fipe_price = fipe_price
        except (TimeoutException, NoSuchElementException) as e:
            log.error(f'Error finding prices (retrying!) [ link: { adv.url } - { traceback.format_exc() }')
            raise e
        except Exception as e:
            log.error(f'Error finding prices [ link: { adv.url } - { traceback.format_exc() }')
