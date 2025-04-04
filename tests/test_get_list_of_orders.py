import requests
import allure
from data.URLs import url
from faker import Faker

fake = Faker()


class TestGetListOfOrders:

    @allure.title('Получение списка заказов')
    @allure.description('Получение списка заказов (код - 200 и "orders" в ответе)')
    def test_get_list_of_orders(self):
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
            "color": fake.random_element(elements=("BLACK", "GREY"))
        }

        # Отправка POST-запроса для создания заказа
        requests.post(f"{url}/api/v1/orders", json=payload)

        # Получение списка заказов
        r = requests.get(f"{url}/api/v1/orders")

        # Проверка статуса ответа и наличия ключа 'orders'
        assert r.status_code == 200
        assert 'orders' in r.json()