from ipaddress import IPv4Address
from whois_ip.get_ip_info import get_information
import time

time_start = time.time()

print(get_information(IPv4Address('36.7.12.5')))
print(get_information('102.155.138.4'))
print(get_information('196.216.205.0'))
print(get_information('1.2.128.0'))
print(get_information('115.246.64.32'))
print(get_information('190.200.0.0'))
print(get_information('186.114.217.0'))
print(get_information('9.1.5.1'))
print(get_information('203.119.42.1'))
print(get_information('192.168.79.1'))
print(get_information('8.25.192.0'))
print(get_information('193.170.79.1'))
print(get_information('209.29.224.3'))
print(get_information('209.29.224.3s'))
print(get_information(('8.8.8.8')))
print(get_information('188.170.86.100'))
print(get_information('193.170.79.0t'))
print(get_information('193.170.79.1'))
print(get_information('192.168.79.1'))
print(time.time() - time_start)
# #
#
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.settimeout(5)
#
# s.connect(('whois.apnic.net', 43))
#
# s.send((bytes('1.2.128.0', 'utf-8')) + b'\r\n')
#
# msg = ''
# while len(msg) < 10000:
#     receive_data = str((s.recv(100)), encoding='utf-8')
#     if (receive_data == ''):
#         break
#     msg = msg + receive_data

# print(msg)
# #
# # {org: { $regex: 'APNIC'}}
# # {netname: { $regex: 'APNIC'}}

# {descr: { $regex: 'APNIC'}}
# {netname: 'APNIC-203'}
