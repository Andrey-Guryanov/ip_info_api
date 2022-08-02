from whois_ip.global_functions.control_arin_ip import handler_arin_api
from whois_ip.global_functions.control_ripe_ip import handler_ripe_api
from whois_ip.global_functions.control_cache import handler_get_cache, handler_save_cache
from whois_ip.global_functions.control_country_info import handler_get_country
from whois_ip.global_functions.control_whois_ip import handler_whois_ip
from whois_ip.apps.sys import settings_load
from whois_ip.apps.ip_app import NoIPError, validation_ip, nslookup_ip
from log_app.custom_logger import logger
import time
SETTINGS = settings_load()


@logger.catch
def get_information(ip):
    s_time = time.time()
    try:
        validation_ip(ip)
    except NoIPError as error:
        logger.error(f'validation error - {error}')
        return {'error': error}
    else:
        check_cache = {}
        if SETTINGS['mongo_cache']:
            check_cache = handler_get_cache(ip)
            logger.debug(f'check_cache = {check_cache}')
        if check_cache == {}:
            get_result = handler_arin_api(ip)
            logger.debug(f'ARIN info = {get_result}')
            netname_split = get_result['netname'].split('-')
            if 'RIPE' in netname_split:
                get_result = handler_ripe_api(ip)
                logger.debug(f'RIPE info  {get_result}')
            elif 'APNIC' in netname_split:
                get_result = handler_whois_ip(SETTINGS['whois_servers']['APNIC'], ip)
                logger.debug(f'APNIC info  {get_result}')
            elif 'LACNIC' in netname_split or (
                    get_result['descr'] is not None and 'http://whois.lacnic.net' in get_result['descr']):
                get_result = handler_whois_ip(SETTINGS['whois_servers']['LACNIC'], ip)
                logger.debug(f'LACNIC info  {get_result}')
            elif 'AFRINIC' in netname_split or get_result['org_name'] == 'African Network Information Center':
                get_result = handler_whois_ip(SETTINGS['whois_servers']['AFRINIC'], ip)
                logger.debug(f'AFRINIC info  {get_result}')
            handler_get_country(get_result)
            if SETTINGS['mongo_cache']:
                handler_save_cache(get_result)
            get_result['ip_req'] = str(ip)
            get_result['host'] = nslookup_ip(ip)
            logger.debug(f'return get info  {get_result}')
            print(f'-------------------{time.time() - s_time}')
            return get_result
        else:
            check_cache['host'] = nslookup_ip(ip)
            check_cache['ip_req'] = str(ip)
            logger.debug(f'return cache info  {check_cache}')
            print(f'-------------------{time.time() - s_time}')
            return check_cache
