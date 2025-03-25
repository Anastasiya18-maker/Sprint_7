import pytest
import requests
import allure
from data.URLs import url
from data.courier_data import generation_new_data_courier
import logging



class TestCreateCourier:

    @allure.title('Создание курьера')
    @allure.step('Проверка создания курьера (код - 201 и текст - "ok": True')
    def test_create_courier(self, registered_courier_data):
        data = generation_new_data_courier()
        data.pop("firstName")  # Удаляем поле для теста
        payload = data
        logging.info(f"Data for courier creation: {data}")

        response = requests.post(f"{url}/api/v1/courier", data=payload)
        assert response.status_code == 201, "Курьер не был создан."
        assert response.json() == {"ok": True}, "Неверное содержимое ответа."

        login_payload = {
            "login": payload["login"],
            "password": payload["password"]
        }
        login_response = requests.post(f"{url}/api/v1/courier/login", data=login_payload)
        assert login_response.status_code == 200, "Login failed."

        courier_id = login_response.json().get("id")
        assert courier_id is not None, "Courier ID not found in login response."

        # Удаление созданного курьера
        delete_response = requests.delete(f"{url}/api/v1/courier/{courier_id}")
        assert delete_response.status_code == 200, "Не удалось удалить курьера."

    @allure.title('Проверка невозможности создать курьера. Дублирующие креды')
    @allure.description('Проверка, что нельзя создать курьера с уже существующими кредами (код - 409 и текст - "message": "Этот логин уже используется. Попробуйте другой."')
    def test_create_courier_duplicate_login(self, registered_courier_data):
        payload = registered_courier_data
        response = requests.post(f"{url}/api/v1/courier", data=payload)

        assert response.status_code == 409, "Курьер с дублирующими данными был создан."
        assert response.json() == {
            "code": 409,
            "message": "Этот логин уже используется. Попробуйте другой."
        }, "Неверное содержимое ответа."

    @allure.title('Проверка невозможности создать курьера. Не все обязательные поля')
    @allure.description(
        'Проверка заполнения не всех обязательных полей. Курьер не создан (код - 400 и текст - "message": "Недостаточно данных для создания учетной записи"')
    def test_create_courier_without_password(self):
        data = generation_new_data_courier()
        payload = {
            "login": data["login"],
            "firstName": data["firstName"]
        }
        response = requests.post(f"{url}/api/v1/courier", data=payload)

        assert response.status_code == 400, "Курьер был создан без обязательных полей."
        assert response.json() == {
            "code": 400,
            "message": "Недостаточно данных для создания учетной записи"
        }, "Неверное содержимое ответа."
