from ipaddress import IPv4Address, IPv4Network
from typing import Optional
from pydantic import BaseModel


class IP(BaseModel):
    ip: IPv4Address


class Whois(BaseModel):
    ip_req: IPv4Address
    network: IPv4Network
    netname: str
    host: Optional[str]
    org_name: Optional[str]
    country_name_ru: Optional[str]
    country_name_en: Optional[str]
    descr: Optional[str]
