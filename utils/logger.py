import logging
from config import LOG_FILE


# Setting up logging
LOG_FILE = "bot.log"  # Путь к файлу для логов

# Creating logger
logger = logging.getLogger(__name__)

# Check to avoid duplicate handlers
if not logger.hasHandlers():
    logger.setLevel(logging.INFO)  # Logging level
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

    # Adding handlers: for console and file
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    file_handler = logging.FileHandler(LOG_FILE)
    file_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)






# # Настройка логов
# logging.basicConfig(
#     level=logging.INFO,
#     format="%(asctime)s - %(levelname)s - %(message)s",
#     handlers=[
#         logging.StreamHandler(),  # Для вывода в консоль
#         logging.FileHandler(LOG_FILE)  # Для записи в файл
#     ]
# )

# logger = logging.getLogger(__name__)

