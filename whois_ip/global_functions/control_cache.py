import os
from time import time, sleep
from threading import Thread
from dotenv import load_dotenv
from whois_ip.apps.sys import settings_load
from whois_ip.apps.sys import create_resp_bogon_net
from whois_ip.custom_class.mongo_db import Mongo_db
from log_app.custom_logger import logger
from whois_ip.apps.ip_app import (
    convert_ip_decimal,
    check_bogon_networks,
    network_ip_first_last,
    convert_decimal_ip,
    validation_ip)

ENV = load_dotenv()
SETTINGS = settings_load()

if SETTINGS['mongo_cache']:
    def clearing_cache():
        logger.debug(f'start thread worker_clearing')
        th = Thread(target=worker_clearing, args=())
        th.daemon = True
        th.start()

    def worker_clearing():
        while True:
            count_clear = CONNECT_MONGO.cache_delete_many(SETTINGS['cache_time_depth'])
            logger.debug(f'cache count_clear = {count_clear}')
            sleep(10800)

    CONNECT_MONGO = Mongo_db(
        {'MONGO_HOST': os.getenv("MONGO_HOST"),
         'MONGO_PORT': int(os.getenv("MONGO_PORT"))},
        'db_whois_ip',
        'cache')
    CONNECT_MONGO.create_index('ip_first')
    CONNECT_MONGO.create_index('ip_last')
    clearing_cache()

@logger.catch()
def handler_save_cache(ip_info):
    cache_data = ip_info.copy()
    cache_data['ip_first'] = convert_ip_decimal(cache_data['ip_first'])
    cache_data['ip_last'] = convert_ip_decimal(cache_data['ip_last'])
    cache_data['time_now'] = time()
    CONNECT_MONGO.insert_data(cache_data)

def create_resp_cache(cache_info):
    del cache_info['_id'], cache_info['time_now']
    cache_info['ip_first'] = str(convert_decimal_ip(cache_info['ip_first']))
    cache_info['ip_last'] = str(convert_decimal_ip(cache_info['ip_last']))
    return cache_info



def handler_get_cache(ip):
    if not validation_ip(ip):
        return {}
    bogon_network = check_bogon_networks(ip)
    if bogon_network:
        result = create_resp_bogon_net(
            bogon_network,
            network_ip_first_last(bogon_network['network']))
        return result

    ip_int =convert_ip_decimal(ip)
    cache_info = CONNECT_MONGO.cache_search_ip(ip_int)
    if len(cache_info) > 0:
        if len(cache_info) == 1:
            return create_resp_cache(cache_info[0])
        else:
            pass
    else:
        return {}
