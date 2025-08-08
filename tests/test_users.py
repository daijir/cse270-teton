import pytest
import httpx

BASE_URL = "http://127.0.0.1:8000"

def test_valid_credentials_should_return_200():
    response = httpx.get(f"{BASE_URL}/users/", params={"username": "admin", "password": "qwerty"})
    assert response.status_code == 200
    assert response.text == ""  # empty response


def test_invalid_credentials_should_return_401():
    response = httpx.get(f"{BASE_URL}/users/", params={"username": "admin", "password": "admin"})
    assert response.status_code == 401
    assert response.text == ""  # empty response
