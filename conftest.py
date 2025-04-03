import pytest
import requests
from data.URLs import url
from data.courier_data import generation_new_data_courier






@pytest.fixture
def courier_data():
    # Регистрация нового курьера и получение данных для входа
    login_pass = generation_new_data_courier()
    courier_info = {
        "login": login_pass["login"],
        "password": login_pass["password"],
        "firstName": login_pass["firstName"]
    }

    # Возвращаем данные курьера
    yield courier_info

    # Очистка созданных данных
    response = requests.post(f"{url}/api/v1/courier/login", data=login_pass)
    if response.status_code == 200:
        courier_id = response.json().get("id")
        if courier_id:
            delete_response=requests.delete(f"{url}/api/v1/courier/{courier_id}")
            assert delete_response.status_code == 200, "Не удалось удалить курьера."






def courier_order_cancel(track):

    cancel_response = requests.put(f"{url}/api/v1/orders/cancel?track={track}")
    print(cancel_response.json())
    assert cancel_response.status_code == 200

@pytest.fixture(scope="session")
def share_data():
    return {"data":None}



