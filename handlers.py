import logging
from aiogram import Dispatcher, types
from aiogram.filters.command import Command
from db.db import SessionLocal
from db.models import User
from datetime import datetime
from services.weather_api import get_weather, get_five_day_forecast


# Command /start
async def send_welcome(message: types.Message):
    welcome_text = (
        "Привет! Я бот, готов помочь тебе с прогнозом погоды.\n"
        "Используй команды:\n"
        "/city <город> — Получение прогноза погоды в написаном городе\n"
        "/weathernow - Получение прогноза погоды в сохраненном городе\n"
        "/settime <часы:минуты> — Установить время для получения прогноза\n"
        "/setcity — Установить город для получения погоды\n"
        "/userinfo — Получить информацию о тебе в боте\n"
    )
    await message.answer(welcome_text)

# Command /city
async def send_weather(message: types.Message):
    """Команда /city - показывает погоду для указанного города."""
    city = message.text.split(' ', 1)[1]
    if not city:
        await message.reply("⚠️ Укажите город после команды `/city`.\nПример: `/city Москва`.")
        return
    weather_report = get_weather(city)
    await message.reply(weather_report)

# Command /week
async def send_week_forecast(message: types.Message):
    city = message.text.split(' ', 1)[1]
    if not city:
        await message.reply('"⚠️ Укажите город после команды `/week`.\nПример: `/week Москва`."')
        return
    week_weather_report = await get_five_day_forecast(city)
    await message.reply(week_weather_report)

# Command /weather_now
async def weather_now(message: types.Message):
    user_id = message.from_user.id
    with SessionLocal() as session:
        user = session.query(User).filter(User.telegram_id == user_id).first()
        
        if user.city:
            weather_info = await get_weather(user.city)
            await message.reply(weather_info)
        else:
            await message.reply("Вы не указали город в своем профиле. Пожалуйста, укажите город с помощью команды /set_city.")

# Command /setcity
async def set_city(message: types.Message):
    city = message.text.split(' ', 1)[1]
    if not city:
        await message.answer("Пожалуйста, укажите город после команды /set_city.")
        return
    
    # Connecting to db
    with SessionLocal() as session:
       user = session.query(User).filter(User.telegram_id == message.from_user.id).first()

    if not user:
        user = User(telegram_id=message.from_user.id, city=city)
        session.add(user)
    else:
        user.city = city
    session.commit()

    await message.answer(f"Город для поиск погоды установлен: {city}")

# Command /settime
async def set_time(message: types.Message):
    time_str = message.text.split(' ', 1)[1]
    try:
        time = datetime.strptime(time_str, "%H:%M").time()
        time_formatted = str(time.strftime("%H:%M"))
    except ValueError:
        await message.answer("Неверный формат времени. Пожалуйста, укажите вреям в формате ЧЧ:ММ.")
        return
    
    # Connecting to db
    try:
        with SessionLocal() as session:
            user = session.query(User).filter(User.telegram_id == message.from_user.id).first()

            if not user:
                user = User(telegram_id=message.from_user.id, time=time_formatted)
                session.add(user)
            else:
                user.time = time_formatted
            session.commit()
        await message.answer(f"Время для уведомлений установлено: {time_formatted}")
    except Exception as e:
        logging.error(f"Error saving time for user {message.from_user.id}: {e}")

# Info about user
async def get_user_info(message: types.Message):
    try:
        with SessionLocal() as session:
            user = session.query(User).filter(User.telegram_id == message.from_user.id).first()

            if user:
                city_info = f"Город: {user.city}" if user.city else "Город не установлен."
                time_info = f"Время уведомлений: {user.time}" if user.time else "Время уведомлений не установлено."
                await message.answer(f"Информация о Вас:\n{city_info}\n{time_info}")
            else:
                await message.answer("Вы не зарегистрированы в системе.")
    except Exception as e:
        logging.error(f"Error: you're not registred {message.from_user.id}: {e}")

# Registration commands
def register_handlers(dp: Dispatcher):
    # Registering commands handlers
    dp.message.register(send_welcome, Command('start'))
    dp.message.register(send_weather, Command('city'))
    dp.message.register(send_week_forecast, Command('week'))
    dp.message.register(weather_now, Command('weathernow'))
    dp.message.register(set_city, Command('setcity'))
    dp.message.register(set_time, Command('settime'))
    dp.message.register(get_user_info, Command("userinfo"))

    
    