# weather_telegram_bot

This project is a Telegram bot that provides users with real-time weather information for a selected city. Users can choose a city and set a specific time to receive weather updates at the same time every day.

## Features:
- Choose a city to get weather forecasts.
- Set a time for receiving regular weather notifications.
- Sends weather notifications through Telegram at the scheduled time.

## Technologies:
- **aiogram**: For interacting with the Telegram API.
- **apscheduler**: For scheduling weather notifications.
- **aiohttp**: For asynchronous HTTP requests.
- **requests**: For fetching weather data from an API.
- **pytz**: For handling time zones.
- **sqlalchemy**: For database operations.
- **sqlite3**: For storing user data and settings.

## Installation:
1. Clone the repository:
    ```bash
    git clone https://github.com/username/weather-telegram-bot.git
    cd weather-telegram-bot
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Set up the bot:
    - Get your bot token from [BotFather](https://core.telegram.org/bots#botfather).
    - Insert the token in the appropriate place in the code.

4. Run the bot:
    ```bash
    python bot.py
    ```

## Usage:
1. Send the `/start` command to the bot to begin.
2. Select a city for weather updates.
3. Set the time to receive notifications.

## License:
This project is licensed under the MIT License.

---

Feel free to replace `username` with your GitHub username and adjust the description according to the specific details of your project.