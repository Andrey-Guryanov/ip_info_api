import click
from whois_ip.get_ip_info import get_information
from whois_ip.apps.sys import (
    parse_ip_tuple,
    parse_ip_str,
    write_result_file)


@click.command()
@click.option("-ip", multiple=True, help="-ip=8.8.8.8")
@click.option("-ip_str", help='-ip_str="8.8.8.8, 8.8.4.4')
@click.option("-result_file", help="-ip=8.8.8.8")
def cmd_get_info(ip=None, ip_str=None, result_file=None):
    ip_addresses = []
    file_data = []
    if ip:
        ip_addresses += parse_ip_tuple(ip)
    if ip_str:
        ip_addresses += parse_ip_str(ip_str)
    ip_addresses = list(set(ip_addresses))
    for ip in ip_addresses:
        ip_info = get_information(ip)
        if result_file and 'error' not in ip_info.keys():
            file_data.append(ip_info)
        write_result_file(result_file, file_data)
        print(ip_info)


if __name__ == '__main__':
    cmd_get_info()

# python cmd_ip_info.py -ip=8.8.8.8 -ip=192.168.1.1 -result_file=test.csv -ip_str="4.5.6.7, 5.6.7.8"
