def test_get_all_duties_for_ksb(ksb_duty_fixture):
    client, ksb, duty, *rest = ksb_duty_fixture
    client.post(f"/api/v1/duties/{duty.id}/ksb/{ksb.id}")
    response = client.get(f"/api/v2/ksb/{ksb.name}")
    
    assert response.status_code == 200
    assert response.get_json() == {
        'ksb_name': ksb.name,
        'linked_to': [duty.name]
    }

def test_get_all_coins_of_non_existent_duty(client):
    name_of_non_existent_ksb = 'Name of non-existent ksb'
    response = client.get(f"/api/v2/ksb/{name_of_non_existent_ksb}")
    
    assert response.status_code == 400
    assert response.get_json() == {
        'error': "Database error",
        'message': f"KSB with name = '{name_of_non_existent_ksb}' does not exist"
    }