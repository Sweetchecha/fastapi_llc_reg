# Используем официальный образ Python в качестве основы
FROM python:3.9-slim

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем все файлы проекта в рабочую директорию
COPY . /app/

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Открываем порт, на котором будет работать приложение
EXPOSE 8000

# Запускаем приложение с помощью Uvicorn (ASGI сервер для FastAPI)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
