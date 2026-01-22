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