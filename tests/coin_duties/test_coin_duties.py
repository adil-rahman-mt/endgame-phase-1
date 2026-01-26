from unittest.mock import MagicMock, patch
import uuid 

valid_uuid = '00000000-0000-4000-a000-000000000000'
invalid_uuid = '1'

def test_get_all_coin_duties(client):
    mock_id = uuid.uuid4()
    mock_coin_id = uuid.uuid4()
    mock_duty_id = uuid.uuid4()
    mock_coins = [{
            "id": str(mock_id),
            "coin_id": str(mock_coin_id),
            "duty_id": str(mock_duty_id),
        },
    ]

    mock_query = MagicMock()
    mock_query.dicts.return_value = mock_coins

    with patch("app.coins.models.Coins.select", return_value=mock_query):
        response = client.get("/coins")
    
    assert response.status_code == 200
    assert response.get_json() == mock_coins

def test_get_record_by_id(coin_duty_resources):
    client, coin_id, duty_id, *rest = coin_duty_resources
    
    new_record_response = client.post("/coin-duties", json={
        "coin_id": coin_id,
        "duty_id": duty_id
    })
    id_of_new_record = new_record_response.get_json()["id"]
    
    get_response = client.get(f"/coin-duties/{id_of_new_record}")
    client.delete(f"/coin-duties/{id_of_new_record}")
    
    assert get_response.get_json() == {
        'id': id_of_new_record,
        'coin_id': coin_id,
        'duty_id': duty_id,
    }

def test_get_non_existent_record(client):
    response = client.get(f"/coin-duties/{valid_uuid}")
    
    assert response.get_json() == {
        'error': "Database error",
        'message': f"A record with ID = {valid_uuid} does not exist"
    }

def test_get_record_with_invalid_id(client):
    response = client.get(f"/coin-duties/{invalid_uuid}")
    
    assert response.get_json() == {
        'error': "Invalid ID format",
        'message': "The provided ID must be a valid UUID"
    }

def test_create_new_record(client):
    mock_id = uuid.uuid4()
    mock_coin_id = uuid.uuid4()
    mock_duty_id = uuid.uuid4()
    mock_coin = {
            "id": str(mock_id),
            "coin_id": str(mock_coin_id),
            "duty_id": str(mock_duty_id)
        }

    mock_model = MagicMock()
    mock_model.id = mock_id
    mock_model.coin_id = MagicMock()
    mock_model.coin_id.id = mock_coin_id
    mock_model.duty_id = MagicMock()
    mock_model.duty_id.id = mock_duty_id

    with patch("app.coin_duties.models.CoinDuties.create", return_value=mock_model):
        response = client.post("/coin-duties", json={
            "coin_id": mock_coin_id,
            "duty_id": mock_duty_id 
        })
    
    assert response.status_code == 201
    assert response.get_json() == mock_coin

def test_create_record_with_non_existent_coin(coin_duty_resources):
    client, _, duty_id, *rest = coin_duty_resources
    new_record_response = client.post("/coin-duties", json={
        "coin_id": valid_uuid,
        "duty_id": duty_id
    })
    
    assert new_record_response.status_code == 400
    assert new_record_response.get_json() == {
            'error': "Input error",
            'message': f"Key (coin_id)=({valid_uuid}) is not present in table \"coins\"."
        }

def test_create_record_with_non_existent_duty(coin_duty_resources):
    client, coin_id, *rest = coin_duty_resources
    new_record_response = client.post("/coin-duties", json={
        "coin_id": coin_id,
        "duty_id": valid_uuid
    })

    assert new_record_response.status_code == 400
    assert new_record_response.get_json() == {
            'error': "Input error",
            'message': f"Key (duty_id)=({valid_uuid}) is not present in table \"duties\"."
        }

def test_create_duplicate_record(coin_duty_resources):
    client, coin_id, duty_id, *rest = coin_duty_resources
    new_record_response = client.post("/coin-duties", json={
        "coin_id": coin_id,
        "duty_id": duty_id
    })
    id_of_new_record = new_record_response.get_json()["id"]
    duplicate_coin_response = client.post("/coin-duties", json={
        "coin_id": coin_id,
        "duty_id": duty_id
    })
    client.delete(f"/coin-duties/{id_of_new_record}")
    
    assert duplicate_coin_response.status_code == 400
    assert duplicate_coin_response.get_json() == {
            'error': "Duplication error",
            'message': f"This record already exists"
        }

def test_delete_existing_record(coin_duty_resources):
    client, coin_id, duty_id, *rest = coin_duty_resources
    post_response = client.post("/coin-duties", json={
        "coin_id": coin_id,
        "duty_id": duty_id
    })
    id_of_coin_duty = post_response.get_json()["id"]
    delete_response = client.delete(f"/coin-duties/{id_of_coin_duty}")
    
    assert delete_response.get_json() == {
        "status": "Success",
        "deleted": {
                'id': id_of_coin_duty,
                'coin_id': coin_id,
                'duty_id': duty_id,
            }
    }

def test_delete_non_existing_record(client):
    response = client.delete(f"/coin-duties/{valid_uuid}")
    
    assert response.get_json() == {
        'error': "Database error",
        'message': f"A record with ID = {valid_uuid} does not exist"
    }
    
def test_delete_record_with_invalid_id(client):
    response = client.delete(f"/coin-duties/{invalid_uuid}")
    
    assert response.get_json() == {
        'error': "Invalid ID format",
        'message': "The provided ID must be a valid UUID"
    }

def test_update_existing_record(coin_duty_resources):
    client, coin_id, duty_id, coin_2_id, duty_2_id = coin_duty_resources
    new_record_response = client.post("/coin-duties", json={
        "coin_id": coin_id,
        "duty_id": duty_id
    })
    id_of_new_record = new_record_response.get_json()["id"]
    patch_response = client.patch(f"/coin-duties/{id_of_new_record}", json={
        "coin_id": coin_2_id,
        "duty_id": duty_2_id
    })
    client.delete(f"coin-duties/{id_of_new_record}")
    
    assert patch_response.get_json() == {
        "id": id_of_new_record,
        "coin_id": coin_2_id,
        "duty_id": duty_2_id
    }

def test_update_non_existing_record(client):
    response = client.patch(f"/coin-duties/{valid_uuid}", json={
        "coin_id": valid_uuid,
        "duty_id": valid_uuid,
    })
    
    assert response.get_json() == {
        'error': "Database error",
        'message': f"A record with ID = {valid_uuid} does not exist"
    }

def test_update_record_with_invalid_id(client):
    response = client.patch(f"/coin-duties/{invalid_uuid}", json={
        "coin_id": valid_uuid,
        "duty_id": valid_uuid,
    })
    
    assert response.get_json() == {
        'error': "Invalid ID format",
        'message': "The provided ID must be a valid UUID"
    }