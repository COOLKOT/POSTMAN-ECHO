import requests
import os
import pytest

def test_post_data():
    data_post = {"name": "Test", "age": 25}
    response = requests.post("https://postman-echo.com/post", json=data_post)
    assert response.status_code == 200
    assert response.json()["json"] == data_post

def test_get_data():
    data_get = {"age": 25}
    response = requests.get("https://postman-echo.com/get", json=data_get)
    assert response.status_code == 400
    assert response.json()["args"]["age"] == 25

def test_incorrect_get_data():
    data_get = {"age": 25}
    response = requests.get("https://postman-echo.com/post", json=data_get)
    assert response.status_code == 404

def test_get_protocol():
    data_get = {"age": 25}
    response = requests.get("https://postman-echo.com/get", json=data_get)
    assert response.status_code == 200
    assert response.json()["headers"]["x-forwarded-proto"] == "https"

test_file = "test_file.txt"

@pytest.fixture
def post_file():
    with open(test_file, "w",) as f:
        f.write("HELLO WORLD")
    yield test_file
    if os.path.exists(test_file):
        os.remove(test_file)


def test_file_sent_with_name_check(post_file):
    with open(post_file, "rb") as f:
        files = {"file": (post_file, f, "text/plain")}
        response = requests.post("https://postman-echo.com/post", files=files, timeout=10)
    assert response.status_code == 200
    response_data = response.json()
    uploaded_files = response_data["files"]
    assert post_file in uploaded_files
    actual_filename = post_file
    assert actual_filename == test_file
