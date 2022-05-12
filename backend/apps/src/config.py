import os
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class JsonConfig:
    with open("{}/config.json".format(BASE_DIR)) as file:
        Data = json.load(file)
    
    @staticmethod
    def get_data(varname, value=None):
        return JsonConfig.Data.get(varname) or value
    
class Config:
    BASE_DIR = BASE_DIR

    DB_USER_NAME=JsonConfig.get_data("DB_USER_NAME", 'root')
    DB_USER_PASSWD=JsonConfig.get_data("DB_USER_PASSWD", 'gistcalculator')
    DB_HOST=JsonConfig.get_data("DB_HOST", 'localhost')
    DB_PORT=JsonConfig.get_data("DB_PORT", '3306')
    DB_NAME=JsonConfig.get_data("DB_NAME", 'test.db')

    @staticmethod
    def database_url(database):
        if database == 'mysql':
            return '{}://{}:{}@{}:{}/{}?charset=utf8'.format('mysql+pymysql', Config.DB_USER_NAME, Config.DB_USER_PASSWD, Config.DB_HOST, Config.DB_PORT, Config.DB_NAME)
