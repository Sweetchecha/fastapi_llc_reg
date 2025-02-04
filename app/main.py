from fastapi import FastAPI, HTTPException, Depends
from app.scraper import register_user
from pydantic import BaseModel
from app.config import Settings
import requests
import time
from fastapi.responses import FileResponse


app = FastAPI()

# Расширенная модель запроса с добавлением всех полей формы
class RegistrationRequest(BaseModel):
    first_name: str  # Имя
    last_name: str  # Фамилия
    company_name: str  # Название компании
    company_address_1: str  # Адрес 1
    company_address_2: str  # Адрес 2
    city: str  # Город
    state: str  # Штат
    zip_code: str  # Почтовый индекс
    country: str  # Страна
    username: str  # Имя пользователя
    email: str  # Электронная почта
    password: str  # Пароль
    re_enter_password: str  # Повторный ввод пароля
    recaptcha_key: str  # Ключ для капчи

# Вспомогательная функция для получения настроек из конфигурации
def get_settings():
    return Settings()

# Функция для решения капчи через 2Captcha
def solve_recaptcha(recaptcha_key: str, google_key: str, page_url: str) -> str:
    url = "https://2captcha.com/in.php"
    params = {
        "key": recaptcha_key,
        "method": "userrecaptcha",
        "googlekey": google_key,  # Google reCAPTCHA ключ сайта
        "pageurl": page_url  # URL страницы с капчей
    }

    # Отправляем запрос на решение капчи
    response = requests.post(url, data=params)
    request_result = response.text.split('|')

    if request_result[0] == 'OK':
        captcha_id = request_result[1]
        time.sleep(20)  # Ждем несколько секунд для получения решения
        result_url = f"https://2captcha.com/res.php?key={recaptcha_key}&action=get&id={captcha_id}"
        result_response = requests.get(result_url)
        result = result_response.text.split('|')
        if result[0] == 'OK':
            return result[1]  # Возвращаем решение капчи
    return None
    
@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse("static/favicon.ico")
    
@app.post("/register")
async def register(request: RegistrationRequest, settings: Settings = Depends(get_settings)):
    try:
        # Проверяем, что пароли совпадают
        if request.password != request.re_enter_password:
            raise HTTPException(status_code=400, detail="Passwords do not match")

        # Проверяем решение капчи
        captcha_solution = solve_recaptcha(request.recaptcha_key, settings.recaptcha_google_key, settings.recaptcha_page_url)
        if not captcha_solution:
            raise HTTPException(status_code=400, detail="Failed to solve captcha")

        # Используем функцию из scraper.py для выполнения регистрации
        success = register_user(
            first_name=request.first_name,
            last_name=request.last_name,
            company_name=request.company_name,
            company_address_1=request.company_address_1,
            company_address_2=request.company_address_2,
            city=request.city,
            state=request.state,
            zip_code=request.zip_code,
            country=request.country,
            email=request.email,
            password=request.password,
            re_enter_password=request.re_enter_password,
            recaptcha_solution=captcha_solution   # Передаем решение капчи
        )

        if not success:
            raise HTTPException(status_code=400, detail="Registration failed")
        
        return {"message": "Registration successful"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))




