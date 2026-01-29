import pytest
from app import create_app
from app.models.coins import Coins
from app.models.duties import Duties
from app.models.ksb import KSB

@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client

@pytest.fixture
def coin_duty_fixture():
    app = create_app()
    app.config["TESTING"] = True

    with app.test_client() as client:
        coin_response = client.post("/api/v1/coins", json={"name": "Test coin name"})
        coin_id = coin_response.get_json()["id"]
        coin_2_response = client.post("/api/v1/coins", json={"name": "Test coin name 2"})
        coin_2_id = coin_2_response.get_json()["id"]
        
        duty_response = client.post("/api/v1/duties", json={
            "name": "Test duty name",
            "description": "Test duty description"
        })
        duty_id = duty_response.get_json()["id"]
        duty_2_response = client.post("/api/v1/duties", json={
            "name": "Test duty name 2",
            "description": "Test duty description 2"
        })
        duty_2_id = duty_2_response.get_json()["id"]

        coin = Coins.get_by_id(coin_id)
        coin_2 = Coins.get_by_id(coin_2_id)
        duty = Duties.get_by_id(duty_id)
        duty_2 = Duties.get_by_id(duty_2_id)
        
        yield client, coin, duty, coin_2, duty_2

        client.delete(f"/api/v1/coins/{coin_id}")
        client.delete(f"/api/v1/coins/{coin_2_id}")
        client.delete(f"/api/v1/duties/{duty_id}")
        client.delete(f"/api/v1/duties/{duty_2_id}")

@pytest.fixture
def ksb_duty_fixture():
    app = create_app()
    app.config["TESTING"] = True

    with app.test_client() as client:
        ksb_response = client.post("/api/v1/ksb", json={
            "type": "Knowledge",
            "name": "Test KSB name",
            "description": "Test KSB description"
        })
        ksb_id = ksb_response.get_json()["id"]
        ksb_2_response = client.post("/api/v1/ksb", json={
            "type": "Skill",
            "name": "Test KSB name 2",
            "description": "Test KSB description 2"
        })
        ksb_2_id = ksb_2_response.get_json()["id"]
        
        duty_response = client.post("/api/v1/duties", json={
            "name": "Test duty name",
            "description": "Test duty description"
        })
        duty_id = duty_response.get_json()["id"]
        duty_2_response = client.post("/api/v1/duties", json={
            "name": "Test duty name 2",
            "description": "Test duty description 2"
        })
        duty_2_id = duty_2_response.get_json()["id"]

        ksb = KSB.get_by_id(ksb_id)
        ksb_2 = KSB.get_by_id(ksb_2_id)
        duty = Duties.get_by_id(duty_id)
        duty_2 = Duties.get_by_id(duty_2_id)
        
        yield client, ksb, duty, ksb_2, duty_2

        client.delete(f"/api/v1/ksb/{ksb_id}")
        client.delete(f"/api/v1/ksb/{ksb_2_id}")
        client.delete(f"/api/v1/duties/{duty_id}")
        client.delete(f"/api/v1/duties/{duty_2_id}")

