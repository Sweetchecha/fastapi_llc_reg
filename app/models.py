import time
import requests
from pydantic import BaseModel
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from fastapi import HTTPException

# Модель запроса для регистрации LLC
class LLCRegistrationRequest(BaseModel):
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

    class Config:
        orm_mode = True  # Разрешает сериализацию модели в формат, подходящий для работы с базой данных

# Функция для решения капчи
def solve_recaptcha(recaptcha_key: str) -> str:
    url = "https://2captcha.com/in.php"
    params = {
        "key": recaptcha_key,
        "method": "userrecaptcha",
        "googlekey": "6LfA1RUaAAAAAG1FUlB7eMlZjGjwcn4vYZpTw4Jv",  # Вставьте ключ Google reCAPTCHA
        "pageurl": "https://example.com"  # URL страницы с капчей
    }

    response = requests.post(url, data=params)
    request_result = response.text.split('|')

    if request_result[0] == 'OK':
        captcha_id = request_result[1]
        time.sleep(20)  # Ожидаем решения капчи
        result_url = f"https://2captcha.com/res.php?key={recaptcha_key}&action=get&id={captcha_id}"
        result_response = requests.get(result_url)
        result = result_response.text.split('|')
        if result[0] == 'OK':
            return result[1]  # Возвращаем решение капчи
    return None

# Функция для регистрации компании
async def register_llc(request: LLCRegistrationRequest):
    try:
        # Извлекаем данные из запроса
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
            re_enter_password = request.re_enter_password
            recaptcha_solution = request.recaptcha_key 

        # Проверка на совпадение пароля и повторного ввода
        if password != reenter_password:
            raise HTTPException(status_code=400, detail="Passwords do not match")

        # Решение капчи
        captcha_solution = solve_recaptcha(recaptcha_key)

        if not captcha_solution:
            raise HTTPException(status_code=400, detail="Failed to solve captcha")

        # Логика регистрации через Selenium
        # Настройки для Firefox
        firefox_options = Options()
        service = Service(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service, options=firefox_options)

        driver.get("https://example.com/registration")  # Замените на нужный URL

        # Заполнение формы
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "first_name"))).send_keys(first_name)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "last_name"))).send_keys(last_name)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "company_name"))).send_keys(company_name)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "company_address_1"))).send_keys(company_address_1)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "company_address_2"))).send_keys(company_address_2)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "city"))).send_keys(city)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "state"))).send_keys(state)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "zip_code"))).send_keys(zip_code)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "country"))).send_keys(country)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "username"))).send_keys(username)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "email"))).send_keys(email)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "password"))).send_keys(password)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "re_enter_password"))).send_keys(reenter_password)

        # Решаем капчу
        captcha_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "g-recaptcha-response")))
        driver.execute_script("arguments[0].style.display = 'block';", captcha_input)  # Показываем поле для капчи
        captcha_input.send_keys(captcha_solution)

        # Отправка формы
        submit_button = driver.find_element(By.ID, "submit_button")
        submit_button.click()

        # Ожидаем успешной регистрации
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "success_message")))

        driver.quit()

        return {"message": "Company registered successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")


