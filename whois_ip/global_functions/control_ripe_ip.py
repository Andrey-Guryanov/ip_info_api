from whois_ip.apps.api_ripe import (
    get_ripe_ip,
    get_ripe_org)
from whois_ip.apps.ip_app import (
    split_ip,
    create_network,
    search_network_by_ip,
    check_bogon_networks,
    network_ip_first_last,
    validation_ip)
from whois_ip.apps.sys_ripe import (
    ripe_unpack_ip_range,
    ripe_unpack_extra_objs,
    ripe_ip_resp_convert)
from whois_ip.apps.sys import create_resp_bogon_net


def handler_ripe_api(ip):
    if not validation_ip(ip):
        return {}

    bogon_network = check_bogon_networks(ip)
    if bogon_network:
        result = create_resp_bogon_net(
            bogon_network,
            network_ip_first_last(bogon_network['network']))
        return result

    resp_ip = get_ripe_ip(ip)
    if not resp_ip:
        return {}

    resp_ripe_net = ripe_unpack_ip_range(resp_ip)
    result_ip = split_ip(resp_ripe_net)
    networks = create_network(result_ip)
    if len(networks) > 1:
        network = str(search_network_by_ip(networks, ip))
    else:
        network = str(networks[0])
    result_ip['network'] = network
    extra_objs = ripe_unpack_extra_objs(resp_ip)
    if 'org' in extra_objs.keys():
        resp_org = get_ripe_org(extra_objs['org'])
    else:
        resp_org = None
    result = ripe_ip_resp_convert(extra_objs, result_ip, resp_org)

    return result
