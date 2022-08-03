from fastapi import APIRouter, Depends
from api.model import IP, Whois
from whois_ip.get_ip_info import get_information
from concurrent.futures import ProcessPoolExecutor
from log_app.custom_logger import logger
import asyncio

router = APIRouter()
API_VERSION = '/api/v1.0'

@router.get(API_VERSION + '/ip_whois/{ip}')
async def ip_whois(ip: IP = Depends(IP)):
    logger.debug(f'get ip_whois ip = {ip}')
    loop = asyncio.get_event_loop()
    with ProcessPoolExecutor() as pool:
        result_whois = await loop.run_in_executor(pool, get_information, ip.ip)
        new_resp = Whois(
            ip_req=result_whois['ip_req'],
            network=result_whois['network'],
            netname=result_whois['netname'],
            host=result_whois['host'],
            org_name=result_whois['org_name'],
            country_name_ru=result_whois['country_name_ru'],
            country_name_en=result_whois['country_name_en'],
            descr=result_whois['descr'])
        logger.debug(f'resp ip_whois {new_resp}')
        return new_resp