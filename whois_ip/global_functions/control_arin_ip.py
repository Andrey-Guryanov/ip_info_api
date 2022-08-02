from whois_ip.apps.sys_arin import (
    arin_ip_resp_convert)
from whois_ip.apps.api_arin import (
    get_arin_ip,
    get_arin_org,
    get_arin_customer)
from whois_ip.apps.ip_app import (
    check_bogon_networks,
    network_ip_first_last,
    validation_ip,
    check_network_by_ip)
from whois_ip.apps.sys import create_resp_bogon_net


def analysis_block_networks(temp_result, ip):
    for network_block in temp_result['arin_networks']:
        if check_network_by_ip(network_block['network'], ip):
            del temp_result['arin_networks']
            return {**network_block, **temp_result}


def handler_arin_api(ip):
    if not validation_ip(ip):
        return {}

    bogon_network = check_bogon_networks(ip)
    if bogon_network:
        result = create_resp_bogon_net(
            bogon_network,
            network_ip_first_last(bogon_network['network']))
        return result

    resp_ip = get_arin_ip(ip)
    resp_org = False
    resp_customer = False
    if not resp_ip:
        return {}

    resp_keys = resp_ip['net'].keys()
    if 'orgRef' in resp_keys:
        org_code = resp_ip['net']['orgRef']['@handle']
        resp_org = get_arin_org(org_code)
    elif 'customerRef' in resp_keys:
        customer_code = resp_ip['net']['customerRef']['@handle']
        resp_customer = get_arin_customer(customer_code)
    temp_result = arin_ip_resp_convert(resp_ip, resp_org, resp_customer)
    result = analysis_block_networks(temp_result, ip)
    return result


if __name__ == '__main__':
    pass
