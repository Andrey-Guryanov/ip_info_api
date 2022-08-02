import requests
from time import time, sleep

URL_API = 'http://rest.db.ripe.net/'
GET_RIPE_TIME = time()-1


def get_ripe_control(func):
    def _wrapper(ip):
        global GET_RIPE_TIME
        while time() - GET_RIPE_TIME < 1:
            sleep(1)
        GET_RIPE_TIME = time()
        return func(ip)
    return _wrapper


@get_ripe_control
def get_ripe_ip(ip):
    response_ip = requests.get(URL_API + f'search.json?&type-filter=inetnum&query-string={ip}')
    if response_ip.status_code == 200:
        get_result = response_ip.json()
    else:
        get_result = False
    return get_result


@get_ripe_control
def get_ripe_org(org_code):
    response_org = requests.get(URL_API + f'ripe/organisation/{org_code}.json')
    if response_org.status_code == 200:
        get_result = response_org.json()
    else:
        get_result = False
    return get_result


if __name__ == '__main__':
    print(get_ripe_ip('87.250.250.242'))
