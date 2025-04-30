from decouple import config

class Config ():
    SECRET_KEY = config('SECRET_KEY')

class Development_Config(Config):
    MYSQL_HOST = config('MYSQL_HOST')
    MYSQL_PORT = config('MYSQL_PORT', cast=int)
    MYSQL_USER = config('MYSQL_USER')
    MYSQL_PASSWORD = config('MYSQL_PASSWORD')
    MYSQL_DB = config('MYSQL_DB')
    MYSQL_PORT = config('MYSQL_PORT', default=3306, cast=int)
    DEBUG = True

config = {
    'development': Development_Config
}