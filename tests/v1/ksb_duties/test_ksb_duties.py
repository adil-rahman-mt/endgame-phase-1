from unittest.mock import MagicMock, patch
import uuid 

valid_uuid = '00000000-0000-4000-a000-000000000000'
invalid_uuid = '1'

def test_get_all(client):
    mock_id = uuid.uuid4()
    mock_ksb_id = uuid.uuid4()
    mock_duty_id = uuid.uuid4()
    mock_ksb_duties = [{
            "id": str(mock_id),
            "ksb_id": str(mock_ksb_id),
            "duty_id": str(mock_duty_id),
        },
    ]

    mock_query = MagicMock()
    mock_query.dicts.return_value = mock_ksb_duties

    with patch("app.api.v1.ksb_duties.models.KsbDuties.select", return_value=mock_query):
        response = client.get("/api/v1/ksb-duties")
    
    assert response.status_code == 200
    assert response.get_json() == mock_ksb_duties

def test_get_by_id(ksb_duty_fixture):
    client, ksb_id, duty_id, *rest = ksb_duty_fixture
    create_ksb_duty_response = client.post("/api/v1/ksb-duties", json={
        "ksb_id": ksb_id,
        "duty_id": duty_id
    })
    id = create_ksb_duty_response.get_json()["id"]
    get_response = client.get(f"/api/v1/ksb-duties/{id}")
    client.delete(f"/api/v1/ksb-duties/{id}")
    
    assert get_response.get_json() == {
        'id': id,
        'ksb_id': ksb_id,
        'duty_id': duty_id,
    }

def test_get_non_existent_record(client):
    response = client.get(f"/api/v1/ksb-duties/{valid_uuid}")
    
    assert response.get_json() == {
        'error': "Database error",
        'message': f"A record with ID = {valid_uuid} does not exist"
    }

def test_get_record_with_invalid_id(client):
    response = client.get(f"/api/v1/ksb-duties/{invalid_uuid}")
    
    assert response.get_json() == {
        'error': "Invalid ID format",
        'message': "The provided ID must be a valid UUID"
    }

def test_create(client):
    mock_id = uuid.uuid4()
    mock_ksb_id = uuid.uuid4()
    mock_duty_id = uuid.uuid4()
    mock_ksb_duty = {
            "id": str(mock_id),
            "ksb_id": str(mock_ksb_id),
            "duty_id": str(mock_duty_id)
        }

    mock_model = MagicMock()
    mock_model.id = mock_id
    mock_model.ksb_id = MagicMock()
    mock_model.ksb_id.id = mock_ksb_id
    mock_model.duty_id = MagicMock()
    mock_model.duty_id.id = mock_duty_id

    with patch("app.api.v1.ksb_duties.models.KsbDuties.create", return_value=mock_model):
        response = client.post("/api/v1/ksb-duties", json={
            "ksb_id": mock_ksb_id,
            "duty_id": mock_duty_id 
        })
    
    assert response.status_code == 201
    assert response.get_json() == mock_ksb_duty

def test_create_with_non_existent_ksb(ksb_duty_fixture):
    client, _, duty_id, *rest = ksb_duty_fixture
    create_ksb_duty_response = client.post("/api/v1/ksb-duties", json={
        "ksb_id": valid_uuid,
        "duty_id": duty_id
    })
    
    assert create_ksb_duty_response.status_code == 400
    assert create_ksb_duty_response.get_json() == {
            'error': "Input error",
            'message': f"Key (ksb_id)=({valid_uuid}) is not present in table \"ksbs\"."
        }

def test_create_with_non_existent_duty(ksb_duty_fixture):
    client, ksb_id, *rest = ksb_duty_fixture
    new_record_response = client.post("/api/v1/ksb-duties", json={
        "ksb_id": ksb_id,
        "duty_id": valid_uuid
    })

    assert new_record_response.status_code == 400
    assert new_record_response.get_json() == {
            'error': "Input error",
            'message': f"Key (duty_id)=({valid_uuid}) is not present in table \"duties\"."
        }

def test_create_duplicate(ksb_duty_fixture):
    client, ksb_id, duty_id, *rest = ksb_duty_fixture
    create_ksb_duty_response = client.post("/api/v1/ksb-duties", json={
        "ksb_id": ksb_id,
        "duty_id": duty_id
    })
    id = create_ksb_duty_response.get_json()["id"]
    duplicate_response = client.post("/api/v1/ksb-duties", json={
        "ksb_id": ksb_id,
        "duty_id": duty_id
    })
    client.delete(f"/api/v1/ksb-duties/{id}")
    
    assert duplicate_response.status_code == 400
    assert duplicate_response.get_json() == {
            'error': "Duplication error",
            'message': f"This record already exists"
        }

def test_delete(ksb_duty_fixture):
    client, ksb_id, duty_id, *rest = ksb_duty_fixture
    create_ksb_duty_response = client.post("/api/v1/ksb-duties", json={
        "ksb_id": ksb_id,
        "duty_id": duty_id
    })
    id = create_ksb_duty_response.get_json()["id"]
    delete_response = client.delete(f"/api/v1/ksb-duties/{id}")
    
    assert delete_response.get_json() == {
        "status": "Success",
        "deleted": {
                'id': id,
                'ksb_id': ksb_id,
                'duty_id': duty_id,
            }
    }

def test_delete_non_existing_record(client):
    response = client.delete(f"/api/v1/ksb-duties/{valid_uuid}")
    
    assert response.get_json() == {
        'error': "Database error",
        'message': f"A record with ID = {valid_uuid} does not exist"
    }
    
def test_delete_record_with_invalid_id(client):
    response = client.delete(f"/api/v1/ksb-duties/{invalid_uuid}")
    
    assert response.get_json() == {
        'error': "Invalid ID format",
        'message': "The provided ID must be a valid UUID"
    }

def test_update(ksb_duty_fixture):
    client, ksb_id, duty_id, ksb_2_id, duty_2_id = ksb_duty_fixture
    create_ksb_duty_response = client.post("/api/v1/ksb-duties", json={
        "ksb_id": ksb_id,
        "duty_id": duty_id
    })
    id = create_ksb_duty_response.get_json()["id"]
    patch_response = client.patch(f"/api/v1/ksb-duties/{id}", json={
        "ksb_id": ksb_2_id,
        "duty_id": duty_2_id
    })
    client.delete(f"/api/v1/ksb-duties/{id}")
    
    assert patch_response.get_json() == {
        "id": id,
        "ksb_id": ksb_2_id,
        "duty_id": duty_2_id
    }

def test_update_non_existing_record(client):
    response = client.patch(f"/api/v1/ksb-duties/{valid_uuid}", json={
        "ksb_id": valid_uuid,
        "duty_id": valid_uuid,
    })
    
    assert response.get_json() == {
        'error': "Database error",
        'message': f"A record with ID = {valid_uuid} does not exist"
    }

def test_update_record_with_invalid_id(client):
    response = client.patch(f"/api/v1/ksb-duties/{invalid_uuid}", json={
        "ksb_id": valid_uuid,
        "duty_id": valid_uuid,
    })
    
    assert response.get_json() == {
        'error': "Invalid ID format",
        'message': "The provided ID must be a valid UUID"
    }