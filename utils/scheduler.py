import logging
import asyncio
import pytz
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from services.weather_api import get_weather
from datetime import datetime
from db.db import SessionLocal
from db.models import User
from aiogram import Bot
from config import BOT_TOKEN


# Setting up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Setting up bot
bot = Bot(token=BOT_TOKEN)

# Func for sending message to users
async def send_weather_message(user):
    if user.time:
        try:
            user_time = user.time
            # Setting up timezone
            timezone = pytz.timezone('Asia/Vladivostok')
            current_time = datetime.now(timezone).strftime("%H:%M")
            
            print(f" Время из БД: {user_time}")
            print(f" Время сейчас: {current_time}")

            # Checking wheather current time matches the time from the time filed
            if user_time == str(current_time):
                city = user.city  # Checking city field for city
                weather_info = await get_weather(city)
                
                # Sending message to user
                await bot.send_message(user.telegram_id, weather_info)
                logger.info(f"Сообщение с погодой отправлено пользователю {user.telegram_id}.")
        except ValueError as e:
            logger.error(f"Ошибка при парсинге времени пользователя {user.telegram_id}: {e}")
        except Exception as e:
            logger.error(f"Неизвестная ошибка при отправке сообщения пользователю {user.telegram_id}: {e}")

# Func checking field 'time'
async def check_time_field():
    try:
        with SessionLocal() as session:
            # Getting all users
            users = session.query(User).all()

            if not users:
                logger.info("В базе данных нет пользователей.")
            else:
                for user in users:
                    if user.time:  # If field 'time' is empty
                        logger.info(f"Поле time не пустое для пользователя {user.telegram_id}.")
                        await send_weather_message(user)
                    else:
                        logger.info(f"В time нет данных для пользователя {user.telegram_id}.")
    except Exception as e:
        logger.error(f"Ошибка при проверке поля 'time': {e}")

# Setting up scheduler
async def start_scheduler():
    loop = asyncio.get_event_loop()  # Событийный цикл
    scheduler = AsyncIOScheduler(event_loop=loop)
    
    # Add task to check time field every minute
    scheduler.add_job(check_time_field, IntervalTrigger(minutes=1), id='check_time_field')
    logger.info("Планировщик добавлен.")
    
    try:
        scheduler.start()  # Running shceduler
        logger.info("Планировщик запущен.")
    except Exception as e:
        logger.error(f"Ошибка при запуске планировщика: {e}")
