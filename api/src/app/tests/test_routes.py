from unittest.mock import patch

import pytest
from app import create_app


@pytest.fixture
def client():
    app = create_app("testing")
    with app.test_client() as client:
        yield client


def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json == {"status": "ok"}


@patch("app.services.external_library.ExternalLibraryService.check_book_status")
def test_book_status(mock_check_status, client):
    mock_check_status.return_value = {"status": "available"}
    response = client.get("/status/1")
    assert response.status_code == 200
    assert response.json["status"] == "available"
