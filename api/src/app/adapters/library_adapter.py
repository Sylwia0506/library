# -*- coding: utf-8 -*-
import os

import requests
from app.exceptions import LibraryServiceError


class LibraryAdapter:

    def __init__(self):
        self.base_url = os.environ.get("LIBRARY_URL", "http://backend:8000")
        self.username = os.environ.get("LIBRARY_USERNAME", "admin")
        self.password = os.environ.get("LIBRARY_PASSWORD", "admin")

    def _get_token(self):
        response = requests.post(
            "{}/api/token/".format(self.base_url),
            json={"username": self.username, "password": self.password},
        )
        if response.status_code != 200:
            raise LibraryServiceError("Nie można uzyskać tokena dostępu")
        return response.json()["access"]

    def _make_request(self, method, endpoint, data=None):
        token = self._get_token()
        headers = {"Content-Type": "application/json"}
        headers["Authorization"] = "Bearer {}".format(token)

        url = "{}/api/{}".format(self.base_url, endpoint)
        response = requests.request(method, url, headers=headers, json=data)

        if response.status_code >= 500:
            raise LibraryServiceError("Błąd serwera głównego systemu bibliotecznego")
        elif response.status_code >= 400:
            raise LibraryServiceError(
                "Błąd w żądaniu do głównego systemu bibliotecznego"
            )

        return response.json()

    def get_book_status(self, book_id):
        return self._make_request("GET", "books/{}/status/".format(book_id))

    def update_book_status(self, book_id, status):
        return self._make_request(
            "PUT", "books/{}/status/".format(book_id), {"status": status}
        )

    def create_reservation(self, book_id, user_id):
        return self._make_request(
            "POST", "reservations/", {"book": book_id, "user": user_id}
        )

    def get_reservation(self, reservation_id):
        return self._make_request("GET", "reservations/{}/".format(reservation_id))

    def verify_token(self, token):
        try:
            response = requests.post(
                "{}/api/token/verify/".format(self.base_url),
                json={"token": token},
                headers={"Content-Type": "application/json"},
            )
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException:
            return False
