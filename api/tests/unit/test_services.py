# -*- coding: utf-8 -*-
import pytest
from app.exceptions import ExternalLibraryError, LibraryServiceError
from app.services.external_library_service import ExternalLibraryService
from mock import patch


def test_check_book_status_success():
    service = ExternalLibraryService()
    book_id = 1

    expected_response = [
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
    ]

    with patch.object(service, "_mock_library_response") as mock_response:

        def mock_side_effect(library_id, _):
            responses = {
                "lib1": {
                    "available": True,
                    "details": {"location": "Section A", "copies": 2},
                },
                "lib2": {
                    "available": False,
                    "details": {"next_available": "2024-03-15"},
                },
            }
            return responses.get(library_id, {})

        mock_response.side_effect = mock_side_effect

        result = service.check_book_status(book_id)
        assert len(result) == len(expected_response)

        sorted_expected = sorted(expected_response, key=lambda x: x["library_id"])
        sorted_result = sorted(result, key=lambda x: x["library_id"])

        for expected, actual in zip(sorted_expected, sorted_result):
            assert expected["library_id"] == actual["library_id"]
            assert expected["available"] == actual["available"]
            assert expected["details"] == actual["details"]
            assert actual["name"] == "Library {}".format(actual["library_id"].upper())


def test_check_book_status_library_error():
    service = ExternalLibraryService()
    book_id = 1

    with patch.object(service, "_mock_library_response") as mock_response:
        mock_response.side_effect = Exception("Connection error")
        result = service.check_book_status(book_id)

        assert len(result) == len(service.libraries)
        assert any(r.get("error") for r in result)


def test_reserve_book_success():
    service = ExternalLibraryService()
    book_id = 1
    library_id = "lib1"
    user_id = "user123"

    expected_response = {
        "reservation_id": "RES123",
        "book_id": book_id,
        "library_id": library_id,
        "user_id": user_id,
        "status": "confirmed",
    }

    result = service.reserve_book(book_id, library_id, user_id)
    assert result == expected_response


def test_reserve_book_all_libraries_failed():
    service = ExternalLibraryService()
    book_id = 1
    library_id = "unknown"
    user_id = "user123"

    with pytest.raises(ExternalLibraryError) as exc_info:
        service.reserve_book(book_id, library_id, user_id)
    assert "Unknown library" in str(exc_info.value)
