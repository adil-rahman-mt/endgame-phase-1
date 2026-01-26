import pytest
from app import create_app
from app.coins.models import Coins

@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client

@pytest.fixture
def coin_duty_resources():
    app = create_app()
    app.config["TESTING"] = True

    with app.test_client() as client:
        coin_response = client.post("/coins", json={"name": "Test coin name"})
        coin_id = coin_response.get_json()["id"]

        coin_2_response = client.post("/coins", json={"name": "Test coin name 2"})
        coin_2_id = coin_2_response.get_json()["id"]
        
        duty_response = client.post("/duties", json={
            "name": "Test duty name",
            "description": "Test duty description"
        })
        duty_id = duty_response.get_json()["id"]

        duty_2_response = client.post("/duties", json={
            "name": "Test duty name 2",
            "description": "Test duty description 2"
        })
        duty_2_id = duty_2_response.get_json()["id"]
        
        yield client, coin_id, duty_id, coin_2_id, duty_2_id

        client.delete(f"/coins/{coin_id}")
        client.delete(f"/coins/{coin_2_id}")
        client.delete(f"/duties/{duty_id}")
        client.delete(f"/duties/{duty_2_id}")

