def test_get_all_coins_for_duty(coin_duty_fixture):
    client, coin, duty, *rest = coin_duty_fixture
    client.post(f"/api/v1/coins/{coin.id}/duties/{duty.id}")
    response = client.get(f"/api/v2/duties/{duty.name}")
    
    assert response.status_code == 200
    assert response.get_json() == {
        'duty_name': duty.name,
        'linked_to': [coin.name]
    }

def test_get_all_coins_of_non_existent_duty(client):
    name_of_non_existent_duty = 'Name of non-existent duty'
    response = client.get(f"/api/v2/duties/{name_of_non_existent_duty}")
    
    assert response.status_code == 400
    assert response.get_json() == {
        'error': "Database error",
        'message': f"Duty with name = '{name_of_non_existent_duty}' does not exist"
    }