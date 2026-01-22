import pytest
from app import app
from unittest.mock import MagicMock, patch
import uuid 

@pytest.fixture
def client():
    with app.test_client() as c:
        yield c

def test_home_route(client):
    response = client.get("/")
    assert response.status_code == 200

def test_get_all_coins(client):
    mock_id = uuid.uuid4()
    mock_coins = [
        {"id": str(mock_id), "name": "Automate"},
    ]

    mock_query = MagicMock()
    mock_query.dicts.return_value = mock_coins

    with patch("app.Coins.select", return_value=mock_query):
        response = client.get("/coins")
    
    assert response.status_code == 200
    assert response.get_json() == mock_coins

def test_get_coin_by_id(client):
    post_response = client.post("/coins", json={"name": "New coin"})
    id_of_new_coin = post_response.get_json()["id"]
    get_response = client.get(f"/coins/{id_of_new_coin}")
    client.delete(f"/coins/{id_of_new_coin}")
    assert get_response.get_json() == {
        "id": id_of_new_coin,
        "name": "New coin",
    }

def test_create_new_coin(client):
    mock_id = uuid.uuid4()
    mock_coin = {"id": str(mock_id) , "name": "Automate"}

    mock_model = MagicMock()
    mock_model.id = mock_id
    mock_model.name = "Automate"

    with patch("app.Coins.create", return_value=mock_model):
        response = client.post("/coins", json={"name": "Automate"})
    
    assert response.status_code == 201
    assert response.get_json() == mock_coin

def test_delete_a_coin(client):
    post_response = client.post("/coins", json={"name": "New coin"})
    id_of_new_coin = post_response.get_json()["id"]
    delete_response = client.delete(f"/coins/{id_of_new_coin}")
    assert delete_response.get_json()["message"] == f"Coin with ID = {id_of_new_coin} has been deleted"