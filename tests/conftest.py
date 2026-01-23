import pytest
from app import create_app
from app.coins.models import Coins

@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client
