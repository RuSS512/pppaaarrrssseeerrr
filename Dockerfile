# Используем официальный лёгкий образ Python 3.9
FROM python:3.9-slim

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Скопируем список зависимостей (requirements.txt) в контейнер
COPY requirements.txt .

# Устанавливаем зависимости из requirements.txt
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Копируем остальные файлы проекта (скрипт и т.д.)
COPY . .

# Указываем команду запуска нашего скрипта
# Если ваш файл называется иначе, замените plushpepe_parser.py на нужный
CMD ["python", "plushpepe_webscraper.py"]
