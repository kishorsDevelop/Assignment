import pytest
from app import app


@pytest.fixture
def client():
    app1 = app({"TESTING": True})
    with app1.test_client() as client:
        yield client