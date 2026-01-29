from unittest.mock import MagicMock, patch
import uuid 

valid_uuid = '00000000-0000-4000-a000-000000000000'
invalid_uuid = '1'

# COINS

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
    
    assert get_response.status_code == 200
    assert get_response.get_json() == {
        "id": id_of_new_coin,
        "name": "Test coin 1",
    }

def test_get_non_existent_coin(client):
    response = client.get(f"/api/v1/coins/{valid_uuid}")
    
    assert response.status_code == 404
    assert response.get_json() == {
        'error': "Database error",
        'message': f"Coin with ID = {valid_uuid} does not exist"
    }

def test_get_coin_with_invalid_id(client):
    response = client.get(f"/api/v1/coins/{invalid_uuid}")
    
    assert response.status_code == 400
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
    
    assert duplicate_coin_response.status_code == 409
    assert duplicate_coin_response.get_json() == {
            'error': "Duplication error",
            'message': "Test coin 1 already exists"
        }

def test_delete_existing_coin(client):
    post_response = client.post("/api/v1/coins", json={"name": "Test coin 1"})
    coin_id = post_response.get_json()["id"]
    coin_name = post_response.get_json()["name"]
    delete_response = client.delete(f"/api/v1/coins/{coin_id}")
    
    assert delete_response.status_code == 200
    assert delete_response.get_json() == {
        "status": "Success",
        "deleted": {
                'id': coin_id,
                'name': coin_name
            }
    }

def test_delete_non_existing_coin(client):
    response = client.delete(f"/api/v1/coins/{valid_uuid}")
    
    assert response.status_code == 404
    assert response.get_json() == {
        'error': "Database error",
        'message': f"Coin with ID = {valid_uuid} does not exist"
    }
    
def test_delete_coin_with_invalid_id(client):
    response = client.delete(f"/api/v1/coins/{invalid_uuid}")
    
    assert response.status_code == 400
    assert response.get_json() == {
        'error': "Invalid ID format",
        'message': "The provided ID must be a valid UUID"
    }

def test_update_existing_coin(client):
    post_response = client.post("/api/v1/coins", json={"name": "New test coin"})
    id_of_new_coin = post_response.get_json()["id"]
    patch_response = client.patch(f"/api/v1/coins/{id_of_new_coin}", json={"name": "Updated test coin"})
    client.delete(f"/api/v1/coins/{id_of_new_coin}")
    
    assert patch_response.status_code == 200
    assert patch_response.get_json() == {
        "id": id_of_new_coin,
        "name": "Updated test coin"
    }

def test_update_non_existing_coin(client):
    response = client.patch(f"/api/v1/coins/{valid_uuid}", json={"name": "Updated coin"})
    
    assert response.status_code == 404
    assert response.get_json() == {
        'error': "Database error",
        'message': f"Coin with ID = {valid_uuid} does not exist"
    }

def test_update_coin_with_invalid_id(client):
    response = client.patch(f"/api/v1/coins/{invalid_uuid}", json={"name": "Updated coin"})
    
    assert response.status_code == 400
    assert response.get_json() == {
        'error': "Invalid ID format",
        'message': "The provided ID must be a valid UUID"
    }

# COIN AND DUTY RELATIONSHIPS

def test_get_all_duties_for_coin(coin_duty_fixture):
    client, coin, duty, *rest = coin_duty_fixture
    client.post(f"/api/v1/coins/{coin.id}/duties/{duty.id}")
    get_duties_for_coin_response = client.get(f"/api/v1/coins/{coin.id}/duties")
    client.delete(f"/api/v1/coins/{coin.id}/duties/{duty.id}")
    
    assert get_duties_for_coin_response.status_code == 200
    assert get_duties_for_coin_response.get_json() == {
        'Coin': coin.name,
        'linked_to': [duty.name]
    }

def test_get_all_duties_for_non_existent_coin(client):
    response = client.get(f"/api/v1/coins/{valid_uuid}/duties")
    
    assert response.status_code == 404
    assert response.get_json() == {
        'error': "Database error",
        'message': f"A coin with ID = {valid_uuid} does not exist"
    }

def test_get_all_duties_for_invalid_coin(client):
    response = client.get(f"/api/v1/coins/{invalid_uuid}/duties")
    
    assert response.status_code == 400
    assert response.get_json() == {
        'error': "Invalid ID format",
        'message': "The provided coin ID must be a valid UUID"
    }

def test_add_duty_to_coin(coin_duty_fixture):
    client, coin, duty, *rest = coin_duty_fixture
    add_duty_to_coin_response = client.post(f"/api/v1/coins/{coin.id}/duties/{duty.id}")
    
    assert add_duty_to_coin_response.status_code == 201
    assert add_duty_to_coin_response.get_json() == {
        'coin_name': coin.name,
        'duty_name': duty.name,
    }

def test_duplication_of_adding_duty_to_coin(coin_duty_fixture):
    client, coin, duty, *rest = coin_duty_fixture
    add_duty_to_coin_response = client.post(f"/api/v1/coins/{coin.id}/duties/{duty.id}")
    duplicate_response = client.post(f"/api/v1/coins/{coin.id}/duties/{duty.id}")
    
    assert duplicate_response.status_code == 409
    assert duplicate_response.get_json() == {
        'error': "Duplication error",
        'message': f"{duty.name} is already associated with {coin.name}"
    }

def test_add_duty_to_non_existent_coin(coin_duty_fixture):
    client, _, duty, *rest = coin_duty_fixture
    add_duty_to_coin_response = client.post(f"/api/v1/coins/{valid_uuid}/duties/{duty.id}")

    assert add_duty_to_coin_response.status_code == 404
    assert add_duty_to_coin_response.get_json() == {
        'error': "Invalid ID",
        'message': f"A coin with ID = {valid_uuid} does not exist"
    }

def test_add_non_existent_duty_to_coin(coin_duty_fixture):
    client, coin, *rest = coin_duty_fixture
    add_duty_to_coin_response = client.post(f"/api/v1/coins/{coin.id}/duties/{valid_uuid}")

    assert add_duty_to_coin_response.status_code == 404
    assert add_duty_to_coin_response.get_json() == {
        'error': "Invalid ID",
        'message': f"A duty with ID = {valid_uuid} does not exist"
    }

def test_add_duty_to_invalid_coin(coin_duty_fixture):
    client, _, duty, *rest = coin_duty_fixture
    add_duty_to_coin_response = client.post(f"/api/v1/coins/{invalid_uuid}/duties/{duty.id}")

    assert add_duty_to_coin_response.status_code == 400
    assert add_duty_to_coin_response.get_json() == {
        'error': "Invalid ID format",
        'message': "IDs must be a valid UUID"
    }

def test_add_invalid_duty_to_coin(coin_duty_fixture):
    client, coin, *rest = coin_duty_fixture
    add_duty_to_coin_response = client.post(f"/api/v1/coins/{coin.id}/duties/{invalid_uuid}")

    assert add_duty_to_coin_response.status_code == 400
    assert add_duty_to_coin_response.get_json() == {
        'error': "Invalid ID format",
        'message': "IDs must be a valid UUID"
    }

def test_remove_duty_from_coin(coin_duty_fixture):
    client, coin, duty, *rest = coin_duty_fixture
    add_duty_to_coin_response = client.post(f"/api/v1/coins/{coin.id}/duties/{duty.id}")
    remove_duty_from_coin_response = client.delete(f"/api/v1/coins/{coin.id}/duties/{duty.id}")

    assert remove_duty_from_coin_response.status_code == 200
    assert remove_duty_from_coin_response.get_json() == {
        'status': "Success",
        'message': f"Removed {duty.name} from {coin.name}",
    }

def test_remove_duty_from_non_existent_coin(coin_duty_fixture):
    client, _, duty, *rest = coin_duty_fixture
    remove_response = client.delete(f"/api/v1/coins/{valid_uuid}/duties/{duty.id}")

    assert remove_response.status_code == 404
    assert remove_response.get_json() == {
        'error': "Invalid ID",
        'message': f"A coin with ID = {valid_uuid} does not exist"
    }

def test_remove_non_existent_duty_from_coin(coin_duty_fixture):
    client, coin, *rest = coin_duty_fixture
    remove_response = client.delete(f"/api/v1/coins/{coin.id}/duties/{valid_uuid}")

    assert remove_response.status_code == 404
    assert remove_response.get_json() == {
        'error': "Invalid ID",
        'message': f"A duty with ID = {valid_uuid} does not exist"
    }

def test_remove_duty_that_is_unassociated_with_coin(coin_duty_fixture):
    client, coin, duty, *rest = coin_duty_fixture
    remove_response = client.delete(f"/api/v1/coins/{coin.id}/duties/{duty.id}")

    assert remove_response.status_code == 404
    assert remove_response.get_json() == {
        'error': "Record does not exist",
        'message': f"{duty.name} is not associated with {coin.name}"
    }

def test_remove_duty_from_invalid_coin(coin_duty_fixture):
    client, _, duty, *rest = coin_duty_fixture
    remove_response = client.delete(f"/api/v1/coins/{invalid_uuid}/duties/{duty.id}")

    assert remove_response.status_code == 400
    assert remove_response.get_json() == {
        'error': "Invalid ID format",
        'message': "IDs must be a valid UUID"
    }

def test_remove_invalid_duty_from_coin(coin_duty_fixture):
    client, coin, *rest = coin_duty_fixture
    remove_response = client.delete(f"/api/v1/coins/{coin.id}/duties/{invalid_uuid}")

    assert remove_response.status_code == 400
    assert remove_response.get_json() == {
        'error': "Invalid ID format",
        'message': "IDs must be a valid UUID"
    }
