import yaml
import csv
from pathlib import Path


def settings_load():
    with open(Path(__file__).parents[2] / r'settings.yaml') as file_settings:
        settings = yaml.load(file_settings, Loader=yaml.FullLoader)
    return settings


def create_resp_bogon_net(bogon_net, bogon_ip):
    result = {
        'ip_first': bogon_ip['ip_first'],
        'ip_last': bogon_ip['ip_last'],
        'network': bogon_net['network'],
        'netname': bogon_net['netname'],
        'country_code': None,
        'country_name_ru': None,
        'country_name_en': None,
        'org_name': None,
        'host': None,
        'descr': bogon_net['descr'],
    }
    return result


def create_resp_whois_ip(custom_inetnum, ip_info):
    result = {
        'ip_first': ip_info['ip_first'],
        'ip_last': ip_info['ip_last'],
        'network': ip_info['network'],
        'netname': custom_inetnum['netname'],
        'country_code': custom_inetnum['country'],
        'org_name': custom_inetnum['org-name'],
        'descr': custom_inetnum['descr'],
    }
    return result


def csv_read_dict(file_patch):
    results = []
    with open(file_patch, 'r', encoding='utf-8') as catalog_file:
        file_reader = csv.DictReader(catalog_file, delimiter=';')
        for row in file_reader:
            results.append(row)
        return results


def parse_ip_tuple(ip_tuple):
    ip_result = [i.strip() for i in ip_tuple]
    return ip_result


def parse_ip_str(ip_str):
    ip_result = [i.strip() for i in ip_str.split(',')]
    return ip_result


def write_result_file(file, data):
    if len(data) > 1:
        with open(file, 'w', newline='', encoding='utf-8') as file_open:
            result_wr = csv.DictWriter(file_open, data[0].keys(), delimiter=';')
            result_wr.writeheader()
            for row in data:
                result_wr.writerow(row)
