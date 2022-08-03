import os
from pathlib import Path
from dotenv import load_dotenv
from whois_ip.apps.sys import settings_load
from whois_ip.apps.sys import csv_read_dict
from whois_ip.custom_class.mongo_db import Mongo_db

ENV = load_dotenv()
SETTINGS = settings_load()
PATH_FILE_COUNTRY_CODE = Path.cwd() / 'whois_ip' / 'local_files' / 'country_code.csv'

if SETTINGS['mongo_cache']:
    CONNECT_MONGO_COUNTRY = Mongo_db(
        {'MONGO_HOST': os.getenv("MONGO_HOST"),
         'MONGO_PORT': int(os.getenv("MONGO_PORT"))},
        'db_whois_ip',
        'catalog_country_code')

    if not CONNECT_MONGO_COUNTRY.check_coll('catalog_country_code'):
        print(PATH_FILE_COUNTRY_CODE)
        print('*****************************')
        db_write_chunk = csv_read_dict(PATH_FILE_COUNTRY_CODE)
        CONNECT_MONGO_COUNTRY.insert_many(db_write_chunk)
        CONNECT_MONGO_COUNTRY.create_index('ALPHA2')

elif not SETTINGS['mongo_cache']:

    country_info = csv_read_dict(PATH_FILE_COUNTRY_CODE)
    countries_directory = {}
    for country in country_info:
        countries_directory[country['ALPHA2']] = {
            'RU_NAME': country['RU_NAME'],
            'EN_NAME': country['EN_NAME'], }


def handler_get_country(ip_info):
    if ip_info['country_code'] is not None:
        if not SETTINGS['mongo_cache']:
            country_name = countries_directory[ip_info['country_code']]
        else:
            country_name = CONNECT_MONGO_COUNTRY.country_infi_search_code(ip_info['country_code'])
            if country_name is None:
                country_name = {'RU_NAME': None, 'EN_NAME': None}

        ip_info['country_name_ru'] = country_name['RU_NAME']
        ip_info['country_name_en'] = country_name['EN_NAME']
    return ip_info
