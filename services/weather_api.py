import aiohttp
from config import WEATHER_API
from datetime import datetime


# Weather for today
async def get_weather(city: str) -> str:
    """Получение погоды для указанного города"""
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API}&units=metric&lang=ru"
    
    # Using aiohttp for asynchronous request
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                main = data['main']
                weather = data['weather'][0]
                return (
                    f"🌍 Город: {city}\n"
                    f"🌡 Температура: {round(main['temp'])}°C\n"
                    f"💧 Влажность: {main['humidity']}%\n"
                    f"📌 Описание: {weather['description'].capitalize()}"
                )
            else:
                return "⚠️ Ошибка! Проверьте правильность названия города."

# Weather for 5 days
async def get_five_day_forecast(city: str) -> str:
    """Получение прогноза погоды на 5 дней для указанного города"""
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={WEATHER_API}&units=metric&lang=ru"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                forecast_list = data['list']
                forecast_text = f"🗓 Прогноз погоды на 5 дней в городе {city}:\n"

                # We go through 5 days (every 3 hours, i.e. 5 days = 5*8 = 40 data)
                for forecast in forecast_list[::8]:  # step 8, since data arrives at 3-hour intervals
                    date = datetime.utcfromtimestamp(forecast['dt']).strftime('%d-%m-%Y %H:%M')
                    temp = round(forecast['main']['temp'])
                    weather_desc = forecast['weather'][0]['description'].capitalize()

                    forecast_text += (
                        f"📅 Время: {date}\n"
                        f"🌡 Температура: {temp}°C\n"
                        f"📌 Описание: {weather_desc}\n\n"
                    )

                return forecast_text
            else:
                return f"⚠️ Ошибка получения данных о прогнозе, статус: {response.status}. Проверьте правильность названия города."