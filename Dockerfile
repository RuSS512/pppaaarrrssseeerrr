# Базовый образ Python (выберите нужную версию)
FROM python:3.9-slim

# Создадим директорию для приложения
WORKDIR /app

# Скопируем список зависимостей
COPY requirements.txt .

# Установим зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Скопируем остальные файлы в контейнер
COPY . .

# Команда, которая будет выполняться при запуске контейнера
CMD ["python", "plushpepe_webscraper.py"]
