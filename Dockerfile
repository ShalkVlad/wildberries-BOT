# Используем базовый образ Python
FROM python:3.9

# Устанавливаем переменную окружения для отображения вывода в терминале
ENV PYTHONUNBUFFERED=1

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Копируем файлы requirements.txt и .env в контейнер
COPY requirements.txt ./
COPY .env ./

# Устанавливаем зависимости Python
RUN pip install --no-cache-dir -r requirements.txt

# Добавляем установку psycopg2-binary
RUN pip install psycopg2-binary

# Копируем все файлы проекта в контейнер
COPY . .

# Запускаем бот
CMD ["python", "bot.py"]
