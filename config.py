import os
from dotenv import load_dotenv


# Загружение переменых окружений
load_dotenv()

BOT_TOKEN = os.getenv('BOT_API')
WEATHER_API = os.getenv('WEATHER_API_KEY')
DB_URL = os.getenv('DB_URL')
LOG_FILE = os.getenv('LOG_FILE')

if not BOT_TOKEN or not WEATHER_API:
    raise ValueError("Отсутствуют BOT_TOKEN или WEATHER_API_KEY в .env файле")

