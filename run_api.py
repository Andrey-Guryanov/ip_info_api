import uvicorn
import os
from fastapi import FastAPI
from api.routers import whois_v1_0
from api.routers import home
from log_app.custom_logger import logger
from whois_ip.apps.sys import settings_load

dir = os.path.abspath(os.curdir)

SETTINGS = settings_load()

app_api = FastAPI()

app_api.include_router(whois_v1_0.router)
app_api.include_router(home.router)


logger.debug('start api')

if __name__ == '__main__':
    uvicorn.run(app_api, host="0.0.0.0", port=SETTINGS['API_PORT'])
