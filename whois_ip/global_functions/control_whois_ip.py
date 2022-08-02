from whois_ip.apps.whois_app import get_server_whois, parser_resp_whois
from whois_ip.apps.sys import create_resp_whois_ip
from whois_ip.apps.ip_app import (
    split_ip,
    create_network,
    validation_network,
    network_ip_first_last)

def handler_whois_ip(whois_hostname, ip):
    whois_resp = (get_server_whois(whois_hostname, str(ip)))
    custom_inetnum = parser_resp_whois(whois_resp)
    if validation_network(custom_inetnum['inetnum']):
        ip_info=network_ip_first_last(custom_inetnum['inetnum'])
        ip_info['network'] = custom_inetnum['inetnum']
    else:
        ip_info = split_ip(custom_inetnum['inetnum'])
        ip_info['network'] = str(create_network(ip_info)[0])
    resp_whois = create_resp_whois_ip(custom_inetnum, ip_info)
    return resp_whois



