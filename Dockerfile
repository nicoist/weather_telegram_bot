# Используем базовый образ на Python, совместимый с арзитектурой ARM (Raspberry Pi)
FROM arm64v8/python:3.11

# Установка рабочей директории в контейнере
WORKDIR /app

# Копирование файлов проекта в контейнер
COPY . /app

# Устанавливаем зависимости из requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Открытие портов, если необходимо (для взаимодействия с ботом)
EXPOSE 8080

# Запуск основного файла bot.py
CMD ["python", "bot.py"]

