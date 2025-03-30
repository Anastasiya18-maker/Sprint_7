import pytest
import requests
from data.URLs import url
from data.courier_data import register_new_courier_and_return_login_password, generation_new_data_courier





@pytest.fixture
def courier_data():
    # Регистрация нового курьера и получение данных для входа
    login_pass = register_new_courier_and_return_login_password()
    courier_info = {
        "login": login_pass[0],
        "password": login_pass[1],
        "firstName": login_pass[2]
    }

    # Возвращаем данные курьера
    yield courier_info

    # Очистка созданных данных
    response = requests.post(f"{url}/api/v1/courier/login", data=login_pass)
    if response.status_code == 200:
        courier_id = response.json().get("id")
        if courier_id:
            requests.delete(f"{url}/api/v1/courier/{courier_id}")


def courier_delete(courier_id, url):
    delete_response = requests.delete(f"{url}/api/v1/courier/{courier_id}")
    assert delete_response.status_code == 200, "Не удалось удалить курьера."



def courier_order_cancel(track):

    cancel_response = requests.put(f"{url}/api/v1/orders/cancel", json = track)
    print(cancel_response.json())
    assert cancel_response.status_code == 200

@pytest.fixture(scope="session")
def share_data():
    return {"data":None}



