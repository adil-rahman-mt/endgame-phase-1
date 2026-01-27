from unittest.mock import MagicMock, patch
import uuid 

valid_uuid = '00000000-0000-4000-a000-000000000000'
invalid_uuid = '1'

def test_get_all_coins(client):
    mock_id = uuid.uuid4()
    mock_coins = [{
            "id": str(mock_id),
            "name": "Mock coin"
        },
    ]

    mock_query = MagicMock()
    mock_query.dicts.return_value = mock_coins

    with patch("app.api.v1.coins.models.Coins.select", return_value=mock_query):
        response = client.get("/api/v1/coins")
    
    assert response.status_code == 200
    assert response.get_json() == mock_coins

def test_get_coin_by_id(client):
    post_response = client.post("/api/v1/coins", json={"name": "Test coin 1"})
    id_of_new_coin = post_response.get_json()["id"]
    get_response = client.get(f"/api/v1/coins/{id_of_new_coin}")
    client.delete(f"/api/v1/coins/{id_of_new_coin}")
    
    assert get_response.get_json() == {
        "id": id_of_new_coin,
        "name": "Test coin 1",
    }

def test_get_non_existent_coin(client):
    response = client.get(f"/api/v1/coins/{valid_uuid}")
    
    assert response.get_json() == {
        'error': "Database error",
        'message': f"Coin with ID = {valid_uuid} does not exist"
    }

def test_get_coin_with_invalid_id(client):
    response = client.get(f"/api/v1/coins/{invalid_uuid}")
    
    assert response.get_json() == {
        'error': "Invalid ID format",
        'message': "The provided ID must be a valid UUID"
    }

def test_create_new_coin(client):
    mock_id = uuid.uuid4()
    mock_coin = {
            "id": str(mock_id),
            "name": "Mock coin"
        }

    mock_model = MagicMock()
    mock_model.id = mock_id
    mock_model.name = "Mock coin"

    with patch("app.api.v1.coins.models.Coins.create", return_value=mock_model):
        response = client.post("/api/v1/coins", json={"name": "Mock coin"})
    
    assert response.status_code == 201
    assert response.get_json() == mock_coin

def test_create_duplicate_coin(client):
    response_1 = client.post("/api/v1/coins", json={"name": "Test coin 1"})
    id_of_new_coin = response_1.get_json()["id"]
    duplicate_coin_response = client.post("/api/v1/coins", json={"name": "Test coin 1"})
    client.delete(f"/api/v1/coins/{id_of_new_coin}")
    
    assert duplicate_coin_response.status_code == 400
    assert duplicate_coin_response.get_json() == {
            'error': "Duplication error",
            'message': "Test coin 1 already exists"
        }

def test_delete_existing_coin(client):
    post_response = client.post("/api/v1/coins", json={"name": "Test coin 1"})
    coin_id = post_response.get_json()["id"]
    coin_name = post_response.get_json()["name"]
    delete_response = client.delete(f"/api/v1/coins/{coin_id}")
    
    assert delete_response.get_json() == {
        "status": "Success",
        "deleted": {
                'id': coin_id,
                'name': coin_name
            }
    }

def test_delete_non_existing_coin(client):
    response = client.delete(f"/api/v1/coins/{valid_uuid}")
    
    assert response.get_json() == {
        'error': "Database error",
        'message': f"Coin with ID = {valid_uuid} does not exist"
    }
    
def test_delete_coin_with_invalid_id(client):
    response = client.delete(f"/api/v1/coins/{invalid_uuid}")
    
    assert response.get_json() == {
        'error': "Invalid ID format",
        'message': "The provided ID must be a valid UUID"
    }

def test_update_existing_coin(client):
    post_response = client.post("/api/v1/coins", json={"name": "New test coin"})
    id_of_new_coin = post_response.get_json()["id"]
    patch_response = client.patch(f"/api/v1/coins/{id_of_new_coin}", json={"name": "Updated test coin"})
    client.delete(f"//api/v1/coins/{id_of_new_coin}")
    
    assert patch_response.get_json() == {
        "id": id_of_new_coin,
        "name": "Updated test coin"
    }

def test_update_non_existing_coin(client):
    response = client.patch(f"/api/v1/coins/{valid_uuid}", json={"name": "Updated coin"})
    
    assert response.get_json() == {
        'error': "Database error",
        'message': f"Coin with ID = {valid_uuid} does not exist"
    }

def test_update_coin_with_invalid_id(client):
    response = client.patch(f"/api/v1/coins/{invalid_uuid}", json={"name": "Updated coin"})
    
    assert response.get_json() == {
        'error': "Invalid ID format",
        'message': "The provided ID must be a valid UUID"
    }