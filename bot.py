import asyncio
from aiogram import Bot, Dispatcher
from db.db import init_db
from config import BOT_TOKEN
from handlers import register_handlers
from utils.logger import logger
from utils.scheduler import start_scheduler


# Creating bot and dispatcher
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

register_handlers(dp)

async def on_start():
    logger.info("Bot has started!")  # Logging launch of bot
    try:
        init_db()  # Initializing database
        logger.info("Database initialized successfully.")
    except Exception as e:
        logger.error(f"Error initializing database: {e}")  # Logging database initialization error
    
    try:
        # Running scheduler in an asynchoronous task
        await start_scheduler()  
        logger.info("Scheduler started successfully.")  # Logging successful launch of scheduler
    except Exception as e:
        logger.error(f"Error starting scheduler: {e}")  # Logging scheduler launch error

    try:
        # Запуск бота
        await dp.start_polling(bot)  # Bot continues work
        logger.info("Polling started. Bot is now running.")  # Logging start of polling
    except Exception as e:
        logger.error(f"Error starting polling: {e}")  # Logging polling launch error

if __name__ == '__main__':
    # Creating event loop and running on_start func
    loop = asyncio.get_event_loop()
    logger.info("Starting bot from bot.py.")  # Logging start of work from bot.py
    try:
        loop.run_until_complete(on_start())
        logger.info("Bot started successfully.")
    except Exception as e:
        logger.error(f"Error during bot startup: {e}")  # Logging error when starting bot
