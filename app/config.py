import os
from dotenv import load_dotenv

# Загружаем переменные окружения из файла .env
load_dotenv()

class Settings:
    # Пример переменных окружения
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./test.db")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "supersecretkey")
    API_KEY: str = os.getenv("API_KEY", "your-api-key")
    recaptcha_key: str = os.getenv("RECAPTCHA_KEY", "your_recaptcha_key")  # Добавляем recaptcha_key
    recaptcha_google_key: str = os.getenv("RECAPTCHA_GOOGLE_KEY")  # Добавьте этот параметр
    recaptcha_page_url: str = os.getenv("RECAPTCHA_PAGE_URL")  # Добавьте этот параметр

# Создаем объект Settings для доступа к переменным окружения
settings = Settings()
