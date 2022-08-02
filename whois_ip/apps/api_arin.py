import requests
from time import time, sleep

URL_API = 'https://whois.arin.net/rest/'
GET_ARIN_TIME = time()-1


def get_arin_control(func):
    def _wrapper(ip):
        global GET_ARIN_TIME
        while time() - GET_ARIN_TIME < 1:
            sleep(1)
        GET_ARIN_TIME = time()
        return func(ip)
    return _wrapper


def _arin_unpack(arin_dict, key_one, key_two):
    value = list(arin_dict[key_one][key_two].values())[0]
    return value


def arin_ip_resp_convert(arin_resp):
    result = {}
    arin_resp = arin_resp['net']
    arin_netblocks = arin_resp['netBlocks']
    cidr_length = _arin_unpack(arin_netblocks, 'netBlock', 'cidrLength')
    if len(arin_netblocks) > 1:
        print(arin_netblocks)
    result['ip_first'] = _arin_unpack(arin_netblocks, 'netBlock', 'startAddress')
    result['ip_last'] = _arin_unpack(arin_netblocks, 'netBlock', 'endAddress')
    result['network'] = f"{result['ip_first']}/{cidr_length}"
    result['netname'] = arin_resp['name']['$']
    print(result)

@get_arin_control
def get_arin_org(org_code):
    response_org = requests.get(URL_API + f'org/{org_code}.json')
    if response_org.status_code == 200:
        return response_org.json()

@get_arin_control
def get_arin_org(org_code):
    response_org = requests.get(URL_API + f'org/{org_code}.json')
    if response_org.status_code == 200:
        get_result = response_org.json()
    else:
        get_result = False
    return get_result

@get_arin_control
def get_arin_customer(customer_code):
    response_customer = requests.get(URL_API + f'customer/{customer_code}.json')
    if response_customer.status_code == 200:
        get_result = response_customer.json()
    else:
        get_result = False
    return get_result

@get_arin_control
def get_arin_ip(ip):
    response_ip = requests.get(URL_API + f'ip/{ip}.json')
    if response_ip.status_code == 200:
        get_result = response_ip.json()
    else:
        get_result = False
    return get_result


if __name__ == '__main__':
    pass
