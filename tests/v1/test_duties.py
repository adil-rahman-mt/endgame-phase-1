from unittest.mock import MagicMock, patch
import uuid 

valid_uuid = '00000000-0000-4000-a000-000000000000'
invalid_uuid = '1'

# DUTIES

def test_get_all_duties(client):
    mock_id = uuid.uuid4()
    mock_duties = [{
            "id": str(mock_id),
            "name": "Mock duty",
            "description": "Mock description"
        },
    ]

    mock_query = MagicMock()
    mock_query.dicts.return_value = mock_duties

    with patch("app.api.v1.duties.routes.Duties.select", return_value=mock_query):
        response = client.get("/api/v1/duties")
    
    assert response.status_code == 200
    assert response.get_json() == mock_duties

def test_get_duty_by_id(client):
    post_response = client.post("/api/v1/duties", json={
            "name": "Test name",
            "description": "Test description"
        })
    id_of_new_duty = post_response.get_json()["id"]
    get_response = client.get(f"/api/v1/duties/{id_of_new_duty}")
    client.delete(f"/api/v1/duties/{id_of_new_duty}")
    
    assert get_response.status_code == 200
    assert get_response.get_json() == {
        "id": id_of_new_duty,
        "name": "Test name",
        "description": "Test description"
    }

def test_get_non_existent_duty(client):
    response = client.get(f"/api/v1/duties/{valid_uuid}")
    
    assert response.status_code == 404
    assert response.get_json() == {
        'error': "Database error",
        'message': f"Duty with ID = {valid_uuid} does not exist"
    }

def test_get_duty_with_invalid_id(client):
    response = client.get(f"/api/v1/duties/{invalid_uuid}")
    
    assert response.status_code == 400
    assert response.get_json() == {
        'error': "Invalid ID format",
        'message': "The provided ID must be a valid UUID"
    }

def test_create_new_duty(client):
    mock_id = uuid.uuid4()
    mock_duty = {
            "id": str(mock_id),
            "name": "Mock duty",
            "description": "Mock description"
        }

    mock_model = MagicMock()
    mock_model.id = mock_id
    mock_model.name = "Mock duty"
    mock_model.description = "Mock description"

    with patch("app.api.v1.duties.routes.Duties.create", return_value=mock_model):
        response = client.post("/api/v1/duties", json={
                "name": "Mock duty",
                "description": "Mock description"
            })
    
    assert response.status_code == 201
    assert response.get_json() == mock_duty

def test_create_duty_with_duplicate_name(client):
    response_1 = client.post("/api/v1/duties", json={
            "name": "Test name",
            "description": "Test description"
        })
    id_of_new_duty = response_1.get_json()["id"]
    duplicate_duty_response = client.post("/api/v1/duties", json={
            "name": "Test name",
            "description": "Test description 2"
        })
    client.delete(f"/api/v1/duties/{id_of_new_duty}")
    
    assert duplicate_duty_response.status_code == 409
    assert duplicate_duty_response.get_json() == {
            'error': "Duplication error",
            'message': "A duty with (name)=(Test name) already exists"
        }

def test_create_duty_with_duplicate_description(client):
    response_1 = client.post("/api/v1/duties", json={
            "name": "Test name",
            "description": "Test description"
        })
    id_of_new_duty = response_1.get_json()["id"]
    duplicate_duty_response = client.post("/api/v1/duties", json={
            "name": "Test name 2",
            "description": "Test description"
        })
    client.delete(f"/api/v1/duties/{id_of_new_duty}")
    
    assert duplicate_duty_response.status_code == 409
    assert duplicate_duty_response.get_json() == {
            'error': "Duplication error",
            'message': "A duty with (description)=(Test description) already exists"
        }

def test_delete_existing_duty(client):
    post_response = client.post("/api/v1/duties", json={
            "name": "Test name",
            "description": "Test description"
        })
    duty_id = post_response.get_json()["id"]
    duty_name = post_response.get_json()["name"]
    duty_description = post_response.get_json()["description"]
    delete_response = client.delete(f"/api/v1/duties/{duty_id}")
    
    assert delete_response.status_code == 200
    assert delete_response.get_json() == {
        "status": "Success",
        "deleted": {
                'id': duty_id,
                'name': duty_name,
                'description': duty_description
            }
    }

def test_delete_non_existing_duty(client):
    response = client.delete(f"/api/v1/duties/{valid_uuid}")
    
    assert response.status_code == 404
    assert response.get_json() == {
        'error': "Database error",
        'message': f"Duty with ID = {valid_uuid} does not exist"
    }
    
def test_delete_duty_with_invalid_id(client):
    response = client.delete(f"/api/v1/duties/{invalid_uuid}")
    
    assert response.status_code == 400
    assert response.get_json() == {
        'error': "Invalid ID format",
        'message': "The provided ID must be a valid UUID"
    }

def test_update_existing_duty(client):
    post_response = client.post("/api/v1/duties", json={
            "name": "Test name",
            "description": "Test description"
        })
    id_of_new_duty = post_response.get_json()["id"]
    patch_response = client.patch(f"/api/v1/duties/{id_of_new_duty}", json={
            "name": "Updated name",
            "description": "Updated description"
        })
    client.delete(f"/api/v1/duties/{id_of_new_duty}")
    
    assert patch_response.status_code == 200
    assert patch_response.get_json() == {
        "id": id_of_new_duty,
        "name": "Updated name",
        "description": "Updated description"
    }

def test_update_non_existing_duty(client):
    response = client.patch(f"/api/v1/duties/{valid_uuid}", json={"name": "Updated duty"})
    
    assert response.status_code == 404
    assert response.get_json() == {
        'error': "Database error",
        'message': f"Duty with ID = {valid_uuid} does not exist"
    }

def test_update_duty_with_invalid_id(client):
    response = client.patch(f"/api/v1/duties/{invalid_uuid}", json={"name": "Updated duty"})
    
    assert response.status_code == 400
    assert response.get_json() == {
        'error': "Invalid ID format",
        'message': "The provided ID must be a valid UUID"
    }

# DUTY AND KSB RELATIONSHIPS

def test_get_all_ksb_for_duty(ksb_duty_fixture):
    client, ksb, duty, *rest = ksb_duty_fixture
    client.post(f"/api/v1/duties/{duty.id}/ksb/{ksb.id}")
    get_ksb_for_duty_response = client.get(f"/api/v1/duties/{duty.id}/ksb")
    client.delete(f"/api/v1/duties/{duty.id}/ksb/{ksb.id}")
    
    assert get_ksb_for_duty_response.status_code == 200
    assert get_ksb_for_duty_response.get_json() == {
        'Duty': duty.name,
        'linked_to': [ksb.name]
    }

def test_get_all_ksb_for_non_existent_duty(client):
    response = client.get(f"/api/v1/duties/{valid_uuid}/ksb")
    
    assert response.status_code == 404
    assert response.get_json() == {
        'error': "Database error",
        'message': f"A duty with ID = {valid_uuid} does not exist"
    }

def test_get_all_ksb_for_invalid_duty(client):
    response = client.get(f"/api/v1/duties/{invalid_uuid}/ksb")
    
    assert response.status_code == 400
    assert response.get_json() == {
        'error': "Invalid ID format",
        'message': "The provided duty ID must be a valid UUID"
    }

def test_add_ksb_to_duty(ksb_duty_fixture):
    client, ksb, duty, *rest = ksb_duty_fixture
    add_ksb_to_duty_response = client.post(f"/api/v1/duties/{duty.id}/ksb/{ksb.id}")
    
    assert add_ksb_to_duty_response.status_code == 201
    assert add_ksb_to_duty_response.get_json() == {
        'duty_name': duty.name,
        'ksb_name': ksb.name,
    }

def test_duplication_of_adding_ksb_to_duty(ksb_duty_fixture):
    client, ksb, duty, *rest = ksb_duty_fixture
    add_ksb_to_duty_response = client.post(f"/api/v1/duties/{duty.id}/ksb/{ksb.id}")
    duplicate_response = client.post(f"/api/v1/duties/{duty.id}/ksb/{ksb.id}")
    
    assert duplicate_response.status_code == 409
    assert duplicate_response.get_json() == {
        'error': "Duplication error",
        'message': f"{ksb.name} is already associated with {duty.name}"
    }

def test_add_ksb_to_non_existent_duty(ksb_duty_fixture):
    client, ksb, *rest = ksb_duty_fixture
    add_ksb_to_duty_response = client.post(f"/api/v1/duties/{valid_uuid}/ksb/{ksb.id}")

    assert add_ksb_to_duty_response.status_code == 404
    assert add_ksb_to_duty_response.get_json() == {
        'error': "Invalid ID",
        'message': f"A duty with ID = {valid_uuid} does not exist"
    }

def test_add_non_existent_ksb_to_duty(ksb_duty_fixture):
    client, _, duty, *rest = ksb_duty_fixture
    add_ksb_to_duty_response = client.post(f"/api/v1/duties/{duty.id}/ksb/{valid_uuid}")

    assert add_ksb_to_duty_response.status_code == 404
    assert add_ksb_to_duty_response.get_json() == {
        'error': "Invalid ID",
        'message': f"A KSB with ID = {valid_uuid} does not exist"
    }

def test_add_ksb_to_invalid_duty(ksb_duty_fixture):
    client, ksb, *rest = ksb_duty_fixture
    add_ksb_to_duty_response = client.post(f"/api/v1/duties/{invalid_uuid}/ksb/{ksb.id}")

    assert add_ksb_to_duty_response.status_code == 400
    assert add_ksb_to_duty_response.get_json() == {
        'error': "Invalid ID format",
        'message': "IDs must be a valid UUID"
    }

def test_add_invalid_ksb_to_duty(ksb_duty_fixture):
    client, _, duty, *rest = ksb_duty_fixture
    add_ksb_to_duty_response = client.post(f"/api/v1/duties/{duty.id}/ksb/{invalid_uuid}")

    assert add_ksb_to_duty_response.status_code == 400
    assert add_ksb_to_duty_response.get_json() == {
        'error': "Invalid ID format",
        'message': "IDs must be a valid UUID"
    }

def test_remove_ksb_from_duty(ksb_duty_fixture):
    client, ksb, duty, *rest = ksb_duty_fixture
    add_ksb_to_duty_response = client.post(f"/api/v1/duties/{duty.id}/ksb/{ksb.id}")
    remove_ksb_from_duty_response = client.delete(f"/api/v1/duties/{duty.id}/ksb/{ksb.id}")

    assert remove_ksb_from_duty_response.status_code == 200
    assert remove_ksb_from_duty_response.get_json() == {
        'status': "Success",
        'message': f"Removed {ksb.name} from {duty.name}",
    }

def test_remove_ksb_from_non_existent_duty(ksb_duty_fixture):
    client, ksb, *rest = ksb_duty_fixture
    remove_response = client.delete(f"/api/v1/duties/{valid_uuid}/ksb/{ksb.id}")

    assert remove_response.status_code == 404
    assert remove_response.get_json() == {
        'error': "Invalid ID",
        'message': f"A duty with ID = {valid_uuid} does not exist"
    }

def test_remove_non_existent_ksb_from_duty(ksb_duty_fixture):
    client, _, duty, *rest = ksb_duty_fixture
    remove_response = client.delete(f"/api/v1/duties/{duty.id}/ksb/{valid_uuid}")

    assert remove_response.status_code == 404
    assert remove_response.get_json() == {
        'error': "Invalid ID",
        'message': f"A KSB with ID = {valid_uuid} does not exist"
    }

def test_remove_duty_that_is_unassociated_with_coin(ksb_duty_fixture):
    client, ksb, duty, *rest = ksb_duty_fixture
    remove_response = client.delete(f"/api/v1/duties/{duty.id}/ksb/{ksb.id}")

    assert remove_response.status_code == 404
    assert remove_response.get_json() == {
        'error': "Record does not exist",
        'message': f"{ksb.name} is not associated with {duty.name}"
    }

def test_remove_ksb_from_invalid_duty(ksb_duty_fixture):
    client, ksb, *rest = ksb_duty_fixture
    remove_response = client.delete(f"/api/v1/duties/{invalid_uuid}/ksb/{ksb.id}")

    assert remove_response.status_code == 400
    assert remove_response.get_json() == {
        'error': "Invalid ID format",
        'message': "IDs must be a valid UUID"
    }

def test_remove_invalid_ksb_from_duty(ksb_duty_fixture):
    client, _, duty, *rest = ksb_duty_fixture
    remove_response = client.delete(f"/api/v1/duties/{duty.id}/ksb/{invalid_uuid}")

    assert remove_response.status_code == 400
    assert remove_response.get_json() == {
        'error': "Invalid ID format",
        'message': "IDs must be a valid UUID"
    }

