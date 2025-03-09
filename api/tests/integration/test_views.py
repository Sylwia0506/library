# -*- coding: utf-8 -*-
import json

import pytest
from app import create_app
from app.exceptions import ExternalLibraryError, LibraryServiceError
from flask_jwt_extended import create_access_token
from mock import patch


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    app.config["JWT_SECRET_KEY"] = "test-key"
    app.config["JWT_ALGORITHM"] = "HS256"
    app.config["JWT_IDENTITY_CLAIM"] = "sub"
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = False

    with app.test_client() as client:
        yield client


@pytest.fixture
def auth_headers(client):
    with client.application.app_context():
        token = create_access_token(identity="test-user")
    return {"Authorization": "Bearer {}".format(token)}


def test_get_book_status_success(client, auth_headers):
    book_id = 1
    expected_response = {
        "book_id": book_id,
        "external_libraries": [
            {
                "library_id": "lib1",
                "name": "Library LIB1",
                "available": True,
                "details": {"location": "Section A", "copies": 2},
            },
            {
                "library_id": "lib2",
                "name": "Library LIB2",
                "available": False,
                "details": {"next_available": "2024-03-15"},
            },
        ],
    }

    with patch(
        "app.services.external_library_service.ExternalLibraryService.check_book_status"
    ) as mock_check:
        with patch(
            "app.adapters.library_adapter.LibraryAdapter.update_book_status"
        ) as mock_update:
            mock_check.return_value = expected_response["external_libraries"]
            mock_update.return_value = {"status": "updated"}

            response = client.get(
                "/api/v1/status/{}".format(book_id), headers=auth_headers
            )

    assert response.status_code == 200
    assert json.loads(response.data) == expected_response


def test_get_book_status_external_error(client, auth_headers):
    book_id = 1

    with patch(
        "app.services.external_library_service.ExternalLibraryService.check_book_status"
    ) as mock_check:
        mock_check.side_effect = ExternalLibraryError("External service unavailable")
        response = client.get("/api/v1/status/{}".format(book_id), headers=auth_headers)

    assert response.status_code == 503
    assert json.loads(response.data)["error"] == "External service unavailable"


def test_reserve_book_success(client, auth_headers):
    request_data = {
        "book_id": 1,
        "user_data": {"name": "Test User", "user_id": "user123"},
    }

    expected_response = {
        "reservation_id": "RES123",
        "book_id": 1,
        "library_id": "lib1",
        "user_id": "user123",
        "status": "confirmed",
    }

    headers = auth_headers.copy()
    headers.update({"Content-Type": "application/json"})

    with patch(
        "app.services.external_library_service.ExternalLibraryService.reserve_book"
    ) as mock_reserve:
        with patch(
            "app.adapters.library_adapter.LibraryAdapter.create_reservation"
        ) as mock_create:
            mock_reserve.return_value = expected_response
            mock_create.return_value = expected_response

            response = client.post(
                "/api/v1/reserve", headers=headers, data=json.dumps(request_data)
            )

    assert response.status_code == 200
    assert json.loads(response.data) == expected_response


def test_reserve_book_invalid_request(client, auth_headers):
    request_data = {}

    headers = auth_headers.copy()
    headers.update({"Content-Type": "application/json"})

    response = client.post(
        "/api/v1/reserve", headers=headers, data=json.dumps(request_data)
    )

    assert response.status_code == 400
    assert json.loads(response.data)["error"] == "Missing book_id in request"


def test_reserve_book_library_error(client, auth_headers):
    request_data = {
        "book_id": 1,
        "user_data": {"name": "Test User", "user_id": "user123"},
    }

    headers = auth_headers.copy()
    headers.update({"Content-Type": "application/json"})

    with patch(
        "app.services.external_library_service.ExternalLibraryService.reserve_book"
    ) as mock_reserve:
        mock_reserve.side_effect = LibraryServiceError("Main system unavailable")

        response = client.post(
            "/api/v1/reserve", headers=headers, data=json.dumps(request_data)
        )

    assert response.status_code == 502
    assert json.loads(response.data)["error"] == "Main system unavailable"
