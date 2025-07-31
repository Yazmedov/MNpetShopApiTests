from http.client import responses

import allure
import jsonschema
import pytest
import requests

BASE_URL = "http://5.181.109.28:9090/api/v3"

from .conftest import create_store
from .schemas.store_schema import STORE_SCHEMA

@allure.feature("Store")
class TestStore:
    @allure.title("Размещение заказа")
    def test_add_order(self):
        with allure.step("Отправка запроса на размещение заказа"):
            payload = {"id": 1,
                       "petId": 1,
                       "quantity": 1,
                       "status": "placed",
                       "complete": True
                       }
            response = requests.post(url=f"{BASE_URL}/store/order", json=payload)
            response_json = response.json()
        with allure.step("Проверка статуса ответа и валидация json-схемы"):
            assert response.status_code == 200
        with allure.step("Проверка параметров заказа в ответе"):
            assert response_json['id'] == payload['id'], "id заказа не совпадает с ожидаемым"
            assert response_json['petId'] == payload['petId'], "petId заказа не совпадает с ожидаемым"
            assert response_json['quantity'] == payload['quantity'], "quantity заказа не совпадает с ожидаемым"
            assert response_json['status'] == payload['status'], "status заказа не совпадает с ожидаемым"
            assert response_json['complete'] == payload['complete'], "complete заказа не совпадает с ожидаемым"

    @allure.title("Получение информации о заказе по ID")
    def test_get_order_by_id(self, create_store):
        with allure.step("Получение ID созданного заказа"):
            store_id = create_store["id"]
        with allure.step("Отправка запроса на получение информации о заказе по ID"):
            response = requests.get(url=f"{BASE_URL}/store/order/1")
        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200
            assert response.json()["id"] == store_id

    @allure.title("Удаление заказа по ID")
    def test_order_delete(self, create_store):
        with allure.step("Получение ID заказа"):
            store_id = create_store["id"]
        with allure.step("Отправка запроса на удаление заказа"):
            response = requests.delete(url=f"{BASE_URL}/store/order/{store_id}")
        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200
        with allure.step("Отправка запроса на получение информации удаленного заказа и проверка статуса ответа"):
            response = requests.get(f"{BASE_URL}/store/order/{store_id}")
            assert response.status_code == 404

    @allure.title("Попытка получить информацию о несуществующем заказе")
    def test_get_info_nonexistent_order(self):
        with allure.step("Отправка запроса на получение информации"):
            response = requests.get(url=f"{BASE_URL}/store/order/9999")
        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 404

    @allure.title("Получение инвентаря магазина")
    def test_get_inventory(self):
        with allure.step("Отправка запроса на получение информации"):
            response = requests.get(url=f"{BASE_URL}/store/inventory")
            response_json = response.json()
        with allure.step("Проверка статуса ответа и валидация json-схемы"):
            assert response.status_code == 200
            jsonschema.validate(response_json, STORE_SCHEMA)



