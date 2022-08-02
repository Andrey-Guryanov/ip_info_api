import ipaddress
import socket


class NoIPError(Exception):
    def __init__(self, message):
        super().__init__(message)


def validation_ip(ip):
    try:
        ipaddress.ip_address(ip)
        result = True
    except ipaddress.AddressValueError:
        raise NoIPError(f'No validation ip {ip}')
    except ValueError:
        raise NoIPError(f'No validation ip {ip}')
    return result


def validation_network(net):
    try:
        ipaddress.IPv4Network(net)
        result = True
    except ipaddress.AddressValueError:
        result = False
    except ValueError:
        result = False
    return result


def convert_ip_decimal(ip):
    if isinstance(ip, str):
        ip = ipaddress.ip_address(ip)
    return int(ip)


def convert_decimal_ip(ip_int):
    ip = ipaddress.ip_address(ip_int)
    return ip


def nslookup_ip(ip):
    try:
        host = socket.gethostbyaddr(str(ip))[0]
    except socket.herror:
        host = None
    return host


def split_ip(ip_str):
    ip_list = ip_str.split('-')
    result = {
        'ip_first': ip_list[0].strip(),
        'ip_last': ip_list[1].strip()
    }
    return result


def network_ip_first_last(net):
    if isinstance(net, str):
        net = ipaddress.IPv4Network(net)
    net = list(net)
    result = {
        'ip_first': str(net[0]).strip(),
        'ip_last': str(net[-1]).strip()
    }
    return result


def create_network(ip_dict):
    result_networks = []
    ip_one = ipaddress.IPv4Address(ip_dict['ip_first'])
    ip_last = ipaddress.IPv4Address(ip_dict['ip_last'])
    for network in ipaddress.summarize_address_range(ip_one, ip_last):
        result_networks.append(network)
    return result_networks


def search_network_by_ip(networks, ip):
    ip = ipaddress.IPv4Address(ip)
    for network in networks:
        search_network = ipaddress.IPv4Network(network)
        if ip in search_network:
            return search_network


def check_network_by_ip(network, ip):
    ip = ipaddress.IPv4Address(ip)
    check_network = ipaddress.IPv4Network(network)
    if ip in check_network:
        return True
    else:
        return False


def check_bogon_networks(ip):
    if isinstance(ip, str):
        ip = ipaddress.IPv4Address(ip)
    bogon_networks = [
        [ipaddress.IPv4Network('0.0.0.0/8'),
         'Reserved IP addresses. Current network.'],
        [ipaddress.IPv4Network('10.0.0.0/8'),
         'Reserved IP addresses. Private network.'],
        [ipaddress.IPv4Network('100.64.0.0/10'),
         'Reserved IP addresses. Private network.'],
        [ipaddress.IPv4Network('127.0.0.0/8'),
         'Reserved IP addresses. Host.'],
        [ipaddress.IPv4Network('169.254.0.0/16'),
         'Reserved IP addresses. Subnet.'],
        [ipaddress.IPv4Network('172.16.0.0/12'),
         'Reserved IP addresses. Private network.'],
        [ipaddress.IPv4Network('192.0.0.0/24'),
         'Reserved IP addresses. Private network.'],
        [ipaddress.IPv4Network('192.0.2.0/24'),
         'Reserved IP addresses. Documentation.'],
        [ipaddress.IPv4Network('192.88.99.0/24'),
         'Reserved IP addresses. Internet.'],
        [ipaddress.IPv4Network('192.168.0.0/16'),
         'Reserved IP addresses. Private network.'],
        [ipaddress.IPv4Network('198.18.0.0/15'),
         'Reserved IP addresses. Private network.'],
        [ipaddress.IPv4Network('198.51.100.0/24'),
         'Reserved IP addresses. Documentation.'],
        [ipaddress.IPv4Network('203.0.113.0/24'),
         'Reserved IP addresses. Internet.'],
        [ipaddress.IPv4Network('233.252.0.0/24'),
         'Reserved IP addresses. Documentation.'],
        [ipaddress.IPv4Network('240.0.0.0/4'),
         'Reserved IP addresses. Internet.'],
        [ipaddress.IPv4Network('255.255.255.255/32'),
         'Reserved IP addresses. Subnet.'], ]
    for network_descr in bogon_networks:
        if ip in network_descr[0]:
            return {'network':
                        str(network_descr[0]),
                    'netname': 'Bogon Network',
                    'descr': network_descr[1] + 'https://en.wikipedia.org/wiki/Reserved_IP_addresses'}
    return False


if __name__ == '__main__':
    print(validation_ip('7.7.7.7'))
    print(validation_ip('7.7.7.7f'))
    print(convert_decimal_ip(134217728))
