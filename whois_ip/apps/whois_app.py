import socket
from log_app.custom_logger import logger

def get_server_whois(whois_hostname, ip, except_count=0):
    try:
        new_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        new_socket.settimeout(5)
        new_socket.connect((whois_hostname, 43))
        new_socket.send((bytes(ip, 'utf-8')) + b'\r\n')
        resp_whois_result = ''
        while len(resp_whois_result) < 100000:
            resp_data = str((new_socket.recv(100)), encoding='utf-8')
            if (resp_data == ''):
                break
            resp_whois_result += resp_data.strip()
        new_socket.close()
    except socket.timeout:
        logger.error(f'socket timeout - server = {whois_hostname}, get ip = {ip}, except_count = {except_count}')
        if except_count <= 3:
            except_count += 1
            get_server_whois(whois_hostname, ip, except_count)
        else:
            resp_whois_result = {}
    logger.debug(f'return socket result = {resp_whois_result}')
    return resp_whois_result


def _check_inetnum(values):
    if 'inetnum' in values:
        return values[1]


def _check_netname(values):
    if 'netname' in values:
        return values[1]
    elif 'ownerid' in values:
        return values[1]


def _check_country(values):
    if 'country' in values and len(values[1]) == 2:
        return values[1]


def _check_org(values):
    if 'org-name' in values:
        return values[1]
    if 'responsible' in values:
        return values[1]


def _check_descr(values, descr):
    if 'descr' in values:
        descr += ' ' + values[1]
    return descr.strip()


def parser_resp_whois(resp_whois):
    resp_whois = resp_whois.splitlines()
    descr_parsing = True

    custom_inetnum = {
        'inetnum': None,
        'netname': None,
        'descr': ' ',
        'country': None,
        'org-name': None}
    for value in resp_whois:
        value = value.split(':')
        if len(value) > 1:
            value[1] = value[1].strip()
            if custom_inetnum['inetnum'] is None:
                custom_inetnum['inetnum'] = _check_inetnum(value)
            if custom_inetnum['netname'] is None:
                custom_inetnum['netname'] = _check_netname(value)
            if custom_inetnum['country'] is None:
                custom_inetnum['country'] = _check_country(value)
            if custom_inetnum['org-name'] is None:
                custom_inetnum['org-name'] = _check_org(value)
            if descr_parsing:
                custom_inetnum['descr'] = _check_descr(value, custom_inetnum['descr'])
        if value[0] == '':
            if custom_inetnum['inetnum'] is not None:
                descr_parsing = False
            elif custom_inetnum['org-name'] is not None:
                break
    return custom_inetnum


if __name__ == '__main__':
    # whois.ripe.net
    # whois.apnic.net

    resp_whois = get_server_whois('whois.apnic.net', '115.246.64.32')
    print(parser_resp_whois(resp_whois))
