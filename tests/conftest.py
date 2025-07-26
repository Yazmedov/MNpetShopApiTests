from http.client import responses

import pytest
import requests

BASE_URL = "http://5.181.109.28:9090/api/v3"

@pytest.fixture(scope="function")
def create_pet():
    payload = {
    "id": 1,
    "name": "Buddy",
    "status": "available"
    }
    response = requests.post(url=f"{BASE_URL}/pet", json=payload)
    assert response.status_code == 200
    return response.json()
@pytest.fixture(scope="function")
def update_pet():
    payload = {
    "id": 1,
    "name": "Buddy Updated",
    "status": "sold"
    }
    response = requests.put(url=f"{BASE_URL}/pet", json=payload)
    assert response.status_code == 200
    return response.json()
@pytest.fixture(scope="function")
def delete_pet():
    payload = {
        "id": 1,
        "name": "Buddy",
        "status": "available"
    }
    response = requests.post(url=f"{BASE_URL}/pet", json=payload)
    assert response.status_code == 200
    response = requests.delete(url=f"{BASE_URL}/pet/1")
    assert response.status_code == 200