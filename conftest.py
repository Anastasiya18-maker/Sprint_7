import pytest
import requests
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from data.URLs import url
from data.courier_data import register_new_courier_and_return_login_password


@pytest.fixture(scope="function")
def driver():
    firefox_options = Options()
    firefox_options.add_argument("--width=1240")
    firefox_options.add_argument("--height=756")

    driver = webdriver.Firefox(options=firefox_options)
    yield driver
    driver.quit()



@pytest.fixture
def registered_courier_data():
    login_pass = register_new_courier_and_return_login_password()
    return {
        "login": login_pass[0],
        "password": login_pass[1],
        "firstName": login_pass[2]
    }

@pytest.fixture
def delete_courier_data():
    login_pass = register_new_courier_and_return_login_password()
    yield {
        "login": login_pass[0],
        "password": login_pass[1]
    }
    response = requests.post(f"{url}/api/v1/courier/login", data=login_pass)
    if response.status_code == 200:
        courier_id = response.json().get("id")
        if courier_id:
            requests.delete(f"{url}/api/v1/courier/{courier_id}")