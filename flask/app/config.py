import os
from dotenv import load_dotenv

# .envファイルを読み込む
load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'password')
    MYSQL_DATABASE_USER = os.getenv('DB_USERNAME')
    MYSQL_DATABASE_PASSWORD = os.getenv('DB_PASSWORD')
    MYSQL_DATABASE_HOST = os.getenv('DB_HOST', 'localhost')
    DEBUG = os.getenv('DEBUG', 'False') == 'True'
