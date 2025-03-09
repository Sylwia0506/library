# -*- coding: utf-8 -*-
import requests
from app.exceptions import ExternalLibraryError


class ExternalLibraryService:
    def __init__(self):
        self.libraries = {
            "lib1": {"url": "http://external-library-1.com", "api_key": "key1"},
            "lib2": {"url": "http://external-library-2.com", "api_key": "key2"},
        }

    def get_book_status(self, book_id, library_id):
        if library_id not in self.libraries:
            raise ExternalLibraryError("Unknown library")
        return {
            "book_id": book_id,
            "library_id": library_id,
            "status": "available",
            "copies": 3,
        }

    def get_library_info(self, lib_id):
        if lib_id not in self.libraries:
            raise ExternalLibraryError("Unknown library")
        return {
            "id": lib_id,
            "name": "Library {}".format(lib_id.upper()),
            "url": self.libraries[lib_id]["url"],
        }

    def reserve_book(self, book_id, library_id, user_id):
        if library_id not in self.libraries:
            raise ExternalLibraryError("Unknown library")
        return {
            "reservation_id": "RES123",
            "book_id": book_id,
            "library_id": library_id,
            "user_id": user_id,
            "status": "confirmed",
        }

    def check_book_availability(self, isbn):
        return self._make_request("GET", "books/{}/availability".format(isbn))

    def check_book_status(self, book_id):
        results = []
        for lib_id in self.libraries:
            try:
                status = self._mock_library_response(lib_id, book_id)
                results.append(
                    {
                        "library_id": lib_id,
                        "name": "Library {}".format(lib_id.upper()),
                        "available": status["available"],
                        "details": status.get("details", {}),
                    }
                )
            except Exception as e:
                results.append(
                    {
                        "library_id": lib_id,
                        "name": "Library {}".format(lib_id.upper()),
                        "error": str(e),
                        "available": False,
                    }
                )
        return results

    def _mock_library_response(self, library_id, book_id):
        if library_id == "lib1":
            return {
                "available": True,
                "details": {"location": "Section A", "copies": 2},
            }
        elif library_id == "lib2":
            return {"available": False, "details": {"next_available": "2024-03-15"}}
        else:
            raise ExternalLibraryError("Unknown library")

    def _mock_reservation(self, library_id, book_id, user_data):
        if library_id == "lib1":
            return {
                "success": True,
                "reservation_id": "{}-{}-123".format(library_id, book_id),
                "details": {
                    "pickup_location": "Main desk",
                    "valid_until": "2024-03-14",
                },
            }
        elif library_id == "lib2":
            return {"success": False, "error": "Book not available"}
        else:
            raise ExternalLibraryError("Unknown library")

    def _make_request(self, method, endpoint, data=None):
        parts = endpoint.split("/")
        lib_id = parts[1]
        if lib_id not in self.libraries:
            raise ExternalLibraryError("Unknown library")
        headers = {
            "Content-Type": "application/json",
            "X-API-Key": self.libraries[lib_id]["api_key"],
        }
        url = "{}/api/{}".format(self.libraries[lib_id]["url"], parts[2])
        response = requests.request(method, url, headers=headers, json=data)
        if response.status_code >= 500:
            raise ExternalLibraryError("External library server error")
        elif response.status_code >= 400:
            raise ExternalLibraryError("Error in request to external library")
        return response.json()
