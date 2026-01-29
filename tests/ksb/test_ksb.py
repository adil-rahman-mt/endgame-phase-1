from unittest.mock import MagicMock, patch
import uuid 

valid_uuid = '00000000-0000-4000-a000-000000000000'
invalid_uuid = '1'

KSB_TYPES = {
    "K": "Knowledge",
    "S": "Skill",
    "B": "Behaviour"
}

def test_get_all_ksbs(client):
    mock_id = uuid.uuid4()
    mock_ksbs = [{
            "id": str(mock_id),
            "type": KSB_TYPES["K"],
            "name": "Mock KSB",
            "description": "Mock description"
        },
    ]

    mock_query = MagicMock()
    mock_query.dicts.return_value = mock_ksbs

    with patch("app.ksb.models.KSB.select", return_value=mock_query):
        response = client.get("/ksb")
    
    assert response.status_code == 200
    assert response.get_json() == mock_ksbs

def test_get_ksb_by_id(client):
    post_response = client.post("/ksb", json={
            "type": KSB_TYPES["K"],
            "name": "Test name",
            "description": "Test description"
        })
    id_of_new_ksb = post_response.get_json()["id"]
    get_response = client.get(f"/ksb/{id_of_new_ksb}")
    client.delete(f"/ksb/{id_of_new_ksb}")
    
    assert get_response.status_code == 200
    assert get_response.get_json() == {
        "id": id_of_new_ksb,
        "type": KSB_TYPES["K"],
        "name": "Test name",
        "description": "Test description"
    }

def test_get_non_existent_ksb(client):
    response = client.get(f"/ksb/{valid_uuid}")
    
    assert response.status_code == 404
    assert response.get_json() == {
        'error': "Database error",
        'message': f"KSB with ID = {valid_uuid} does not exist"
    }

def test_get_ksb_with_invalid_id(client):
    response = client.get(f"/ksb/{invalid_uuid}")
    
    assert response.status_code == 400
    assert response.get_json() == {
        'error': "Invalid ID format",
        'message': "The provided ID must be a valid UUID"
    }

def test_create_new_ksb(client):
    mock_id = uuid.uuid4()
    mock_ksb = {
            "id": str(mock_id),
            "type": KSB_TYPES["K"],
            "name": "Mock KSB",
            "description": "Mock description"
        }

    mock_model = MagicMock()
    mock_model.id = mock_id
    mock_model.type = KSB_TYPES["K"]
    mock_model.name = "Mock KSB"
    mock_model.description = "Mock description"

    with patch("app.ksb.models.KSB.create", return_value=mock_model):
        response = client.post("/ksb", json={
                "type": KSB_TYPES["K"],
                "name": "Mock KSB",
                "description": "Mock description"
            })
    
    assert response.status_code == 201
    assert response.get_json() == mock_ksb

def test_create_ksb_with_duplicate_name(client):
    response_1 = client.post("/ksb", json={
            "type": KSB_TYPES["K"],
            "name": "Test name",
            "description": "Test description"
        })
    id_of_new_ksb = response_1.get_json()["id"]
    duplicate_ksb_response = client.post("/ksb", json={
            "type": KSB_TYPES["K"],
            "name": "Test name",
            "description": "Test description 2"
        })
    client.delete(f"/ksb/{id_of_new_ksb}")
    
    assert duplicate_ksb_response.status_code == 409
    assert duplicate_ksb_response.get_json() == {
            'error': "Duplication error",
            'message': "A KSB with (name)=(Test name) already exists"
        }

def test_create_ksb_with_duplicate_description(client):
    response_1 = client.post("/ksb", json={
            "type": KSB_TYPES["K"],
            "name": "Test name",
            "description": "Test description"
        })
    id_of_new_ksb = response_1.get_json()["id"]
    duplicate_ksb_response = client.post("/ksb", json={
            "type": KSB_TYPES["K"],
            "name": "Test name 2",
            "description": "Test description"
        })
    client.delete(f"/ksb/{id_of_new_ksb}")
    
    assert duplicate_ksb_response.status_code == 409
    assert duplicate_ksb_response.get_json() == {
            'error': "Duplication error",
            'message': "A KSB with (description)=(Test description) already exists"
        }

def test_create_ksb_with_invalid_type(client):
    response = client.post("/ksb", json={
            "type": "Invalid KSB type",
            "name": "Test name",
            "description": "Test description"
        })
    
    assert response.status_code == 400
    assert response.get_json() == {
            'error': "Invalid type",
            'message': "Type must be one of 'Knowledge', 'Skill' or 'Behaviour'",
        }

def test_delete_existing_ksb(client):
    post_response = client.post("/ksb", json={
            "type": KSB_TYPES["K"],
            "name": "Test name",
            "description": "Test description"
        })
    ksb_id = post_response.get_json()["id"]
    ksb_type = post_response.get_json()["type"]
    ksb_name = post_response.get_json()["name"]
    ksb_description = post_response.get_json()["description"]
    delete_response = client.delete(f"/ksb/{ksb_id}")
    
    assert delete_response.status_code == 200
    assert delete_response.get_json() == {
        "status": "Success",
        "deleted": {
                'id': ksb_id,
                'type': ksb_type,
                'name': ksb_name,
                'description': ksb_description
            }
    }

def test_delete_non_existing_ksb(client):
    response = client.delete(f"/ksb/{valid_uuid}")
    
    assert response.status_code == 404
    assert response.get_json() == {
        'error': "Database error",
        'message': f"KSB with ID = {valid_uuid} does not exist"
    }
    
def test_delete_ksb_with_invalid_id(client):
    response = client.delete(f"/ksb/{invalid_uuid}")
    
    assert response.status_code == 400
    assert response.get_json() == {
        'error': "Invalid ID format",
        'message': "The provided ID must be a valid UUID"
    }

def test_update_existing_ksb(client):
    post_response = client.post("/ksb", json={
            "type": KSB_TYPES["K"],
            "name": "Test name",
            "description": "Test description"
        })
    id_of_new_ksb = post_response.get_json()["id"]
    patch_response = client.patch(f"/ksb/{id_of_new_ksb}", json={
            "type": KSB_TYPES["S"],
            "name": "Updated name",
            "description": "Updated description"
        })
    client.delete(f"ksb/{id_of_new_ksb}")
    
    assert patch_response.status_code == 200
    assert patch_response.get_json() == {
        "id": id_of_new_ksb,
        "type": KSB_TYPES["S"],
        "name": "Updated name",
        "description": "Updated description"
    }

def test_update_non_existing_ksb(client):
    response = client.patch(f"/ksb/{valid_uuid}", json={"name": "Updated ksb"})
    
    assert response.status_code == 404
    assert response.get_json() == {
        'error': "Database error",
        'message': f"KSB with ID = {valid_uuid} does not exist"
    }

def test_update_ksb_with_invalid_id(client):
    response = client.patch(f"/ksb/{invalid_uuid}", json={"name": "Updated ksb"})
    
    assert response.status_code == 400
    assert response.get_json() == {
        'error': "Invalid ID format",
        'message': "The provided ID must be a valid UUID"
    }

def test_update_ksb_with_invalid_type(client):    
    post_response = client.post("/ksb", json={
            "type": KSB_TYPES["K"],
            "name": "Test name",
            "description": "Test description"
        })
    id_of_new_ksb = post_response.get_json()["id"]
    patch_response = client.patch(f"/ksb/{id_of_new_ksb}", json={
            "type": "Invalid KSB type",
            "name": "Updated name",
            "description": "Updated description"
        })
    client.delete(f"ksb/{id_of_new_ksb}")
    
    assert patch_response.status_code == 400
    assert patch_response.get_json() == {
            'error': "Invalid type",
            'message': "Type must be one of 'Knowledge', 'Skill' or 'Behaviour'",
        }