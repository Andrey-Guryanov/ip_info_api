from time import time
from pymongo import MongoClient, errors
from log_app.custom_logger import logger

def autoreconnect_retry(fun, count_max_except=3):
    def db_op_wrapper(*args, **kwargs):
        count_except = 0
        while count_except < count_max_except:
            try:
                return fun(*args, **kwargs)
            except errors.AutoReconnect:
                logger.error(f'AutoReconnect, fun_name = {fun.__name__}, count_except = {count_except}')
                count_except += 1
        raise Exception("No luck even after %d retries" % count_max_except)
    return db_op_wrapper

class Mongo_db:
    def __init__(self, mongo_connect, db_name, collection_name):
        self.connect_mongo = MongoClient(mongo_connect['MONGO_HOST'],
                                         mongo_connect['MONGO_PORT'],
                                         serverSelectionTimeoutMS=10000,
                                         directConnection=True)
        self.connect_db = self.connect_mongo[db_name]
        self.collection = self.connect_db[collection_name]

    def insert_data(self, data):
        self.collection.insert_one(data)

    def create_index(self, value_name, unique=True):
        self.collection.create_index(value_name, unique=unique)

    def check_coll(self, coll_name):
        if coll_name in self.connect_db.list_collection_names():
            return True
        else:
            return False
    @autoreconnect_retry
    def cache_search_ip(self, ip, count_except=0):
        logger.debug(f'cache_search_ip ip_int = {ip}')
        result = []
        for value in self.collection.find(
                {"$and":
                    [
                        {"ip_first": {"$lte": ip}},
                        {"ip_last": {"$gte": ip}}
                    ]
                }
        ):
            result.append(value)
            logger.debug(f'cache_search_ip value = {value}')
        return result

    @autoreconnect_retry
    def country_infi_search_code(self, country_code, count_except=0):
        country_name = self.collection.find_one({"ALPHA2": country_code},
                                                {"_id": 0, "RU_NAME": 1, "EN_NAME": 1})
        return country_name

    def check_coll(self, coll_name):
        if coll_name in self.connect_db.list_collection_names():
            return True
        else:
            return False

    def insert_many(self, values):
        self.collection.insert_many(values, ordered=False)

    def cache_delete_many(self, storage_depth):
        check_time = time() - storage_depth
        count_delete_doc = self.collection.delete_many({"time_now": {"$lt": check_time}})
        return count_delete_doc
