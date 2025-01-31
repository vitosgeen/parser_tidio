# data for environment variables from .env file

import os

from dotenv import load_dotenv

class Config:
    TIDIO_LOGIN = ""
    TIDIO_PASSWORD = ""
    USER_DATA_DIR = ""
    USER_DOWNLOAD_DIR = ""
    TIDIO_API_TOKEN = ""
    TIDIO_API_KEY = ""
    TIDIO_TIME_ZONE = ""

    
    def __init__(self):
        self.load_from_env_file()
        # check if the environment variables are set up
        if not self.TIDIO_LOGIN:
            raise ValueError('TIDIO_LOGIN is not set') 
        if not self.TIDIO_PASSWORD:
            raise ValueError('TIDIO_PASSWORD is not set')
        if not self.USER_DATA_DIR:
            raise ValueError('USER_DATA_DIR is not set')
        if not self.TIDIO_API_TOKEN:
            raise ValueError('TIDIO_API_TOKEN is not set')
        if not self.TIDIO_API_KEY:
            raise ValueError('TIDIO_API_KEY is not set')
        if not self.TIDIO_TIME_ZONE:
            raise ValueError('TIDIO_TIME_ZONE is not set')
        if not self.USER_DOWNLOAD_DIR:
            raise ValueError('USER_DOWNLOAD_DIR is not set')
            

    def load_from_env_file(self):
        # set .env file path
        load_dotenv()
        self.TIDIO_LOGIN = os.getenv('TIDIO_LOGIN')
        self.TIDIO_PASSWORD = os.getenv('TIDIO_PASSWORD')   
        self.USER_DATA_DIR = os.getenv('USER_DATA_DIR')
        self.TIDIO_API_TOKEN = os.getenv('TIDIO_API_TOKEN')
        self.TIDIO_API_KEY = os.getenv('TIDIO_API_KEY')
        self.TIDIO_TIME_ZONE = os.getenv('TIDIO_TIME_ZONE')
        self.USER_DOWNLOAD_DIR = os.getenv('USER_DOWNLOAD_DIR')
    
    def get_tidio_login(self):
        return self.TIDIO_LOGIN
    
    def get_tidio_password(self):
        return self.TIDIO_PASSWORD
    
    def get_user_data_dir(self):
        return  self.USER_DATA_DIR
    
    def get_tidio_api_token(self):
        return self.TIDIO_API_TOKEN
    
    def get_tidio_api_key(self):
        return self.TIDIO_API_KEY
    
    def get_tidio_time_zone(self):
        return self.TIDIO_TIME_ZONE
    
    def get_user_download_dir(self):
        return self.USER_DOWNLOAD_DIR
    
    def get_cookie_str(self):
        return self.COOKIE_STR
    