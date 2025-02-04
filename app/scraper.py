import time
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests

def solve_recaptcha(recaptcha_key: str) -> str:
    """
    Функция для решения капчи с помощью стороннего API.
    Нужно передать ключ для API, который будет решать капчу.
    """
    url = "https://2captcha.com/in.php"
    params = {
        "key": recaptcha_key,
        "method": "userrecaptcha",
        "googlekey": "6LfA1RUaAAAAAG1FUlB7eMlZjGjwcn4vYZpTw4Jv",  # Здесь вставьте ключ сайта от Google reCAPTCHA
        "pageurl": "https://example.com"  # URL страницы с капчей
    }
    
    response = requests.post(url, data=params)
    request_result = response.text.split('|')
    
    if request_result[0] == 'OK':
        captcha_id = request_result[1]
        # Получаем решение через некоторое время
        time.sleep(20)  # Подождите 20 секунд перед получением решения
        result_url = f"https://2captcha.com/res.php?key={recaptcha_key}&action=get&id={captcha_id}"
        result_response = requests.get(result_url)
        result = result_response.text.split('|')
        if result[0] == 'OK':
            return result[1]  # Возвращаем решение капчи
    return None

def register_user(first_name: str, last_name: str, organization: str, address1: str, address2: str, 
                  city: str, state: str, zip_code: str, country: str, email: str, password: str, 
                  reenter_password: str, recaptcha_key: str) -> bool:
    """
    Регистрация пользователя на сайте.
    """
    # Настройки для Firefox
    firefox_options = Options()
    # Включаем безголовый режим (если нужно)
    # firefox_options.headless = True

    # Установка драйвера Firefox с помощью GeckoDriver
    service = Service(GeckoDriverManager().install())
    driver = webdriver.Firefox(service=service, options=firefox_options)

    try:
        # Открываем страницу регистрации
        driver.get("https://example.com/registration")

        # Заполняем поля формы
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "first_name"))).send_keys(first_name)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "last_name"))).send_keys(last_name)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "organization"))).send_keys(organization)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "address1"))).send_keys(address1)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "address2"))).send_keys(address2)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "city"))).send_keys(city)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "state"))).send_keys(state)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "zip"))).send_keys(zip_code)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "country"))).send_keys(country)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "email"))).send_keys(email)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "password"))).send_keys(password)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "re_enter_password"))).send_keys(reenter_password)

        # Решаем капчу
        captcha_solution = solve_recaptcha(recaptcha_key)

        if captcha_solution:
            # Вводим решение капчи в соответствующее поле
            captcha_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "g-recaptcha-response")))
            driver.execute_script("arguments[0].style.display = 'block';", captcha_input)  # Включаем поле для капчи
            captcha_input.send_keys(captcha_solution)

            # Отправляем форму
            submit_button = driver.find_element(By.ID, "submit_button")
            submit_button.click()

            # Ждем подтверждения успешной регистрации
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "success_message")))

            print("Регистрация успешна!")
            return True
        else:
            print("Не удалось решить капчу.")
            return False
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        return False
    finally:
        driver.quit()

# Пример использования
if __name__ == "__main__":
    # Примерные данные для регистрации
    first_name = "John"
    last_name = "Doe"
    company_name = "SomeOrg"
    company_address_1 = "123 Some St"
    company_address_2 = "Apt 456"
    city = "Some City"
    state = "Some State"
    zip_code = "12345"
    country = "Country"
    email = "your-email@example.com"
    password = "your_password"
    re_enter_password = "your_password"
    recaptcha_key = "your_2captcha_api_key"  # Вставьте свой API ключ от 2Captcha
    
    success = register_user(first_name, last_name, organization, address1, address2, city, state, zip_code, 
                            country, email, password, reenter_password, recaptcha_key)
    if success:
        print("Пользователь успешно зарегистрирован.")
    else:
        print("Регистрация не удалась.")
