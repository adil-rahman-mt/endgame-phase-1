import pytest
from app import app

@pytest.fixture
def client():
    with app.test_client() as c:
        yield c

def test_home_route(client):
    response = client.get("/")
    assert response.status_code == 200

def test_get_all_coins(client):
    response = client.get("/coins")
    assert response.status_code == 200

def test_create_new_coin(client):
    response = client.post("/coins", json={
        "name": "Automate",
    })
    assert response.status_code == 201
    print(response.get_json())
    assert len(response.get_json()) == 2