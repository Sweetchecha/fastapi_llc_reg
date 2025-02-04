# LLC Registration API

## Описание

Этот проект предоставляет API для регистрации компаний в форме ООО (общество с ограниченной ответственностью). API позволяет отправлять данные для регистрации компании, включая название компании, адрес, информацию о директоре и другие данные. Для защиты формы регистрации используется Google reCAPTCHA, которая проверяется через сторонний сервис (например, 2Captcha). Проект разработан с использованием FastAPI для обеспечения высокой производительности и быстрого отклика.

## Функциональность

- Регистрация компании с заполнением формы.
- Защита от автоматических регистраций с помощью Google reCAPTCHA.
- Решение капчи с использованием стороннего сервиса (2Captcha).
- Реализация через FastAPI для быстрой и эффективной обработки запросов.
- Использование Pydantic для валидации данных.

## Структура проекта

```plaintext
.
├── app/
│   ├── __init__.py        # Инициализация модуля
│   ├── main.py            # Главный файл с FastAPI приложением и маршрутами
│   ├── models.py          # Модели данных для запроса и ответа
│   ├── config.py          # Настройки и конфигурации проекта
│   ├── scraper.py         # Скрипт для заполнения формы через Selenium
│   ├── utils.py           # Вспомогательные функции
├── tests/
│   ├── test_api.py        # Тесты для API с использованием pytest
├── .env                   # Переменные окружения (например, для ключей API)
├── Dockerfile             # Конфигурация для Docker
├── requirements.txt       # Зависимости проекта
├── README.md              # Этот файл

## Установка

    git clone https://github.com/Sweetchecha/fastapi_llc_registration.git
    cd fastapi_llc_registration

Для установки всех зависимостей проекта, выполните команду:

    pip install -r requirements.txt

Создайте файл .env в корне проекта и добавьте в него следующие переменные:

    DATABASE_URL=sqlite:///./test.db
    SECRET_KEY=supersecretkey
    API_KEY=your-api-key
    RECAPTCHA_SECRET_KEY=your-2captcha-api-key

## Запуск приложения

    Для запуска приложения используйте Uvicorn:

    uvicorn app.main:app --reload

## Запуск приложения(Docker)

    Откройте терминал в корне вашего проекта (где находится Dockerfile), и выполните следующую команду для создания Docker образа:

    docker build -t fastapi_llc_registration

    После того как образ собран, можно запустить контейнер:

    docker run -d -p 8000:8000 llc-registration-api

Эндпоинт для регистрации нового пользователя.

    curl -X 'POST' 'http://127.0.0.1:8000/register'   -H 'Content-Type: application/json'   -d '{
        "first_name": "John",
        "last_name": "Doe",
        "username": "johndoe",
        "company_name": "SomeOrg",
        "company_address_1": "123 Some St",
        "company_address_2": "Apt 456",
        "city": "Some City",
        "state": "Some State",
        "zip_code": "12345",
        "country": "Country",
        "email": "your-email@example.com",
        "password": "your_password",
        "re_enter_password": "your_password",
        "recaptcha_key": "your_2captcha_api_key"
    }'

Ответ :

    200 OK : Успешная регистрация пользователя.
    400 Bad Request : Ошибка при решении капчи или несоответствие паролей.
    500 Internal Server Error : Ошибка на сервере.

##Структура API

    Регистрация пользователя :
        Входные данные для регистрации включают личные данные, контактные данные и данные для входа.
        Для решения капчи используется сторонняя сервис 2Captcha.
        Регистрация осуществляется через внешний процесс (например, заполнение форм на сайте).

    Защита с помощью reCAPTCHA :
        Для предотвращения автоматической регистрации применяется система защиты от ботов (reCAPTCHA).
        Решение капчи происходит через API-сервис 2Captcha, для чего требуется ключ API, который передается в теле запроса.

##Файл .env

    DATABASE_URL="sqlite:///./test.db"
    SECRET_KEY="supersecretkey"
    API_KEY="your-api-key"
    RECAPTCHA_KEY="your_recaptcha_key"
    RECAPTCHA_GOOGLE_KEY="your_google_recaptcha_key"
    RECAPTCHA_PAGE_URL="https://example.com/register"
