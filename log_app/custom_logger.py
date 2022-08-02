import os
from loguru import logger
from dotenv import load_dotenv

ENV = load_dotenv()

logger.add('logs/logs.log', format='>>  {time:DD-MM-YYYY HH:mm:ss:SSS}  {file}  {function}  {line}  {level}  >// {message} <//',
           level=os.getenv('LEVEL'), rotation=os.getenv('ROTATION'), compression='zip')