import requests
import allure
import pytest
from data.URLs import url
from faker import Faker

fake = Faker()

class TestCreateOrder:

    @pytest.mark.parametrize('color', [
        ['BLACK'],
        ['GREY'],
        ['BLACK', 'GRAY'],
        []
    ])
    @allure.title('Создание заказа')
    @allure.description('Проверка создания заказа (код - 201 и track в ответе)')
    def test_create_order(self, color):
        # Генерация случайных данных с помощью Faker
        payload = {
            "firstName": fake.first_name(),
            "lastName": fake.last_name(),
            "address": fake.address(),
            "metroStation": fake.random_int(min=1, max=10),
            "phone": fake.phone_number(),
            "rentTime": fake.random_int(min=1, max=10),
            "deliveryDate": fake.date_between(start_date='today', end_date='+30d').isoformat(),
            # Дата доставки в будущем
            "comment": fake.sentence(),
            "color": color
        }

        # Отправка POST-запроса для создания заказа
        r = requests.post(f"{url}/api/v1/orders", json=payload)

        # Проверка статуса ответа и наличия ключа 'track'
        assert r.status_code == 201
        assert 'track' in r.json()