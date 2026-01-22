import pytest
from app import app

@pytest.fixture
def client():
    with app.test_client() as c:
        yield c

def test_home_route(client):
    response = client.get("/")
    assert response.status_code == 200