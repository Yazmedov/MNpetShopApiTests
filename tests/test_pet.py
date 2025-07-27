from http.client import responses

import allure
import jsonschema
import requests

from .conftest import create_pet
from .schemas.pet_schema import PET_SCHEMA

BASE_URL = "http://5.181.109.28:9090/api/v3"

@allure.feature("Pet")
class TestPet:
    @allure.title("Попытка удалить несуществующего питомца")
    def test_delete_nonexistent_pet(self):
        with allure.step("Отправка запроса на удаление несуществующего питомца"):
            response = requests.delete(url=f"{BASE_URL}/pet/9999")

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200, "код ответа не совпал с ожидаемым"

        with allure.step("Проверка текстового содержимого ответа"):
                assert response.text == "Pet deleted", "текст ошибки не совпал с ожидаемым"

    @allure.title("Попытка обновить несуществующего питомца")
    def test_update_nonexistent_pet(self):
        with allure.step("Отправка запроса на обновление несуществующего питомца"):
            payload = {"id": 999999,
                       "name": "Non-existent Pet",
                       "status": "available"
                       }

            response = requests.put(url=f"{BASE_URL}/pet", json=payload)

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 404, "код ответа не совпал с ожидаемым"

        with allure.step("Проверка текстового содержимого ответа"):
            assert response.text == "Pet not found", "текст ошибки не совпал с ожидаемым"

    @allure.title("Добавление нового питомца")
    def test_add_pet(self):
        with allure.step("Подготовка данных для создания питомца"):
            payload = {"id": 1,
                       "name": "Buddy",
                       "status": "available"
                       }

        with allure.step("отправка запроса на создание питомца"):
            response = requests.post(url=f"{BASE_URL}/pet", json=payload)
            response_json = response.json()

        with allure.step("Проверка статуса ответа и валидация json-схемы"):
            assert response.status_code == 200

            jsonschema.validate(response_json, PET_SCHEMA)

        with allure.step("Проверка параметров питомцев в ответе"):
            assert response_json['id'] == payload['id'], "id питомцев не совпадает с ожидаемым"
            assert response_json['name'] == payload['name'], "name питомцев не совпадает с ожидаемым"
            assert response_json['status'] == payload['status'], "status питомцев не совпадает с ожидаемым"

    @allure.title("добавление нового питомца с полными данными")
    def test_add_pet_fulldata(self):
        with allure.step("Подготовка данных для создания питомца"):
            payload = {"id": 10,
                       "name": "doggie",
                       "category": {"id": 1, "name": "Dogs"},
                       "photoUrls": ["string"],
                       "tags": [{"id": 0, "name": "string"}],
                       "status": "available"}
        with allure.step("Отправка запроса на создание питомца с полными данными"):
            response = requests.post(url=f"{BASE_URL}/pet", json=payload)
            response_json = response.json()
        with allure.step("Проверка статуса ответа и валидация json-схемы"):
            assert response.status_code == 200
            jsonschema.validate(response_json, PET_SCHEMA)
        with allure.step("Проверка параметров питомцев в ответе"):
            assert response_json['id'] == payload['id'], "id питомцев не совпадает с ожидаемым"
            assert response_json['name'] == payload['name'], "name питомцев не совпадает с ожидаемым"
            assert response_json['category'] == payload['category'], "category питомцев не совпадает с ожидаемым"
            assert response_json['photoUrls'] == payload['photoUrls'], "photoUrls питомцев не совпадает с ожидаемым"
            assert response_json['tags'] == payload['tags'], "tags питомцев не совпадает с ожидаемым"
            assert response_json['status'] == payload['status'], "status питомцев не совпадает с ожидаемым"

    @allure.title("Получение информации о питомце по ID")
    def test_pet_get_by_id(self, create_pet):
        with allure.step("Получение ID созданного питомца"):
            pet_id = create_pet["id"]
        with allure.step("Отправка запроса на получение информации о питомце по ID"):
            response = requests.get(f"{BASE_URL}/pet/{pet_id}")
        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200
            assert response.json()["id"] == pet_id

    @allure.title("Обновление питомца")
    def test_pet_update(self, create_pet):
        with allure.step("Получение ID созданного питомца"):
            pet_id = create_pet["id"]
        with allure.step("Отправка запроса на получение информации о питомце по ID"):
            response = requests.get(f"{BASE_URL}/pet/{pet_id}")
        with allure.step("Отправка запроса на обновление питомца"):
            payload = {"id": 1,
                       "name": "Buddy Updated1",
                       "status": "sold"
                       }
            response = requests.put(url=f"{BASE_URL}/pet/", json=payload)
        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200
            response_json = response.json()
        with allure.step("Проверка полей"):
            assert response_json['id'] == payload['id'], "id питомцев не совпадает с ожидаемым"
            assert response_json['name'] == payload['name'], "name питомцев не совпадает с ожидаемым"
            assert response_json['status'] == payload['status'], "status питомцев не совпадает с ожидаемым"
    @allure.title("Удаление питомца")
    def test_pet_delete(self, create_pet):
        with allure.step("Получение ID созданного питомца"):
            pet_id = create_pet["id"]
        with allure.step("Отправка запроса на получение информации о питомце по ID"):
            response = requests.get(f"{BASE_URL}/pet/{pet_id}")
        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200
        with allure.step("Отправка запроса на удаление питомца"):
            response = requests.delete(url=f"{BASE_URL}/pet/{pet_id}")
        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200
        with allure.step("Отправка запроса на получение информации удаленного питомца и проверка статуса ответа"):
            response = requests.get(f"{BASE_URL}/pet/{pet_id}")
            assert response.status_code == 404

