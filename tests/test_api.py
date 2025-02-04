import pytest
from fastapi.testclient import TestClient
from app.main import app
from unittest.mock import patch

client = TestClient(app)

@pytest.fixture
def mock_recaptcha():
    """
    Мок для функции решения капчи. Моделирует успешное решение капчи.
    """
    with patch("app.main.solve_recaptcha") as mock:
        mock.return_value = "dummy_solution"  # Моделируем успешное решение капчи
        yield mock

def test_register_success(mock_recaptcha):
    """
    Тест для успешной регистрации с валидным запросом.
    """
    response = client.post(
        "/register",
        json={
            "first_name": "John",
            "last_name": "Doe",
            "company_name": "Test Company",
            "company_address_1": "123 Main St",
            "company_address_2": "Suite 100",
            "city": "Test City",
            "state": "Test State",
            "zip_code": "12345",
            "country": "Test Country",
            "username": "johndoe",
            "email": "test@example.com",
            "password": "testpassword",
            "re_enter_password": "testpassword",
            "recaptcha_key": "dummy_recaptcha_key",
        },
    )

    assert response.status_code == 200
    assert response.json() == {"message": "Registration successful"}
    mock_recaptcha.assert_called_once()  # Убедитесь, что функция решения капчи была вызвана

def test_register_failed_recaptcha(mock_recaptcha):
    """
    Тест для случая, когда капча не может быть решена.
    """
    # Мокаем функцию, чтобы она возвращала None (неудачное решение капчи)
    mock_recaptcha.return_value = None

    response = client.post(
        "/register",
        json={
            "first_name": "John",
            "last_name": "Doe",
            "company_name": "Test Company",
            "company_address_1": "123 Main St",
            "company_address_2": "Suite 100",
            "city": "Test City",
            "state": "Test State",
            "zip_code": "12345",
            "country": "Test Country",
            "username": "johndoe",
            "email": "test@example.com",
            "password": "testpassword",
            "re_enter_password": "testpassword",
            "recaptcha_key": "dummy_recaptcha_key",
        },
    )

    assert response.status_code == 400
    assert response.json() == {"detail": "Failed to solve captcha"}
    mock_recaptcha.assert_called_once()  # Убедитесь, что функция решения капчи была вызвана

def test_register_missing_fields(mock_recaptcha):
    """
    Тест для случая, когда запрос содержит недостаточно данных.
    """
    response = client.post(
        "/register",
        json={
            "first_name": "John",
            "last_name": "Doe",
            "company_name": "Test Company",
            "company_address_1": "123 Main St",
            "company_address_2": "Suite 100",
            "city": "Test City",
            "state": "Test State",
            "zip_code": "12345",
            # Отсутствует поле "country"
            "username": "johndoe",
            "email": "test@example.com",
            "password": "testpassword",
            "re_enter_password": "testpassword",
            "recaptcha_key": "dummy_recaptcha_key",
        },
    )

    assert response.status_code == 422  # Ошибка валидации данных
    assert "detail" in response.json()

def test_register_internal_server_error():
    """
    Тест для имитации внутренней ошибки сервера.
    """
    # Мокаем функцию решения капчи, чтобы она выбрасывала исключение
    with patch("app.main.solve_recaptcha", side_effect=Exception("Internal Server Error")):
        response = client.post(
            "/register",
            json={
                "first_name": "John",
                "last_name": "Doe",
                "company_name": "Test Company",
                "company_address_1": "123 Main St",
                "company_address_2": "Suite 100",
                "city": "Test City",
                "state": "Test State",
                "zip_code": "12345",
                "country": "Test Country",
                "username": "johndoe",
                "email": "test@example.com",
                "password": "testpassword",
                "re_enter_password": "testpassword",
                "recaptcha_key": "dummy_recaptcha_key",
            },
        )

    assert response.status_code == 500
    assert response.json() == {"detail": "Internal Server Error: Internal Server Error"}

def test_invalid_recaptcha_key():
    """
    Тест для случая с невалидным ключом капчи.
    """
    response = client.post(
        "/register",
        json={
            "first_name": "John",
            "last_name": "Doe",
            "company_name": "Test Company",
            "company_address_1": "123 Main St",
            "company_address_2": "Suite 100",
            "city": "Test City",
            "state": "Test State",
            "zip_code": "12345",
            "country": "Test Country",
            "username": "johndoe",
            "email": "test@example.com",
            "password": "testpassword",
            "re_enter_password": "testpassword",
            "recaptcha_key": "invalid_recaptcha_key",
        },
    )

    assert response.status_code == 400
    assert response.json() == {"detail": "Failed to solve captcha"}



