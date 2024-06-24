from fastapi import FastAPI
from fastapi.testclient import TestClient
app = FastAPI(
    title="Common api"
)


ENG_TXT = "This is a test message in English this test will test whether the application can generate a summary." \
          "If the  text is short, the application will return it as a summary"

client = TestClient(app)


def test_get_base_page():
    response = client.get("https://summarytextpy-9kn5rcfzhb463uwgjdp5s3.streamlit.app/")
    json_data = response.json()
    assert response.status_code == 200
    assert json_data["message"] == "Welcome to Base Page"
def test_post_eng_text():
    response = client.post("/summary_text/", json={"text": ENG_TXT})
    json_data = response.json()
    assert response.status_code == 200
    assert json_data['Краткое содержание:'] == "This is a test message in English."
def test_post_rus_text():
    response = client.post("/summary_text/", json={"text": "Тестовая строка"})
    json_data = response.json()
    assert response.status_code == 200
    assert json_data['Краткое содержание:'] == "Тест теста"
def test_post_empty_string():
    response = client.post("/summary_text/", json={"text": ""})
    json_data = response.json()
    assert response.status_code == 200
    assert json_data['Краткое содержание:'] == "Пустая строка"
def test_error_empty_json():
    response = client.post("/summary_text/", json={})
    json_data = response.json()
    assert response.status_code == 422
    assert json_data['detail'][0]['type'] == "missing"
    assert json_data['detail'][0]['loc'] == ["body", "text"]
    assert json_data['detail'][0]['msg'] == "Field required"
