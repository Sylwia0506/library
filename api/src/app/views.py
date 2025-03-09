# -*- coding: utf-8 -*-
from app.adapters.library_adapter import LibraryAdapter
from app.exceptions import ExternalLibraryError, LibraryServiceError
from app.services.external_library_service import ExternalLibraryService
from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_optional, jwt_required
from flask_restful import Resource

library_adapter = LibraryAdapter()
external_library_service = ExternalLibraryService()


class BookStatus(Resource):
    @jwt_required
    def get(self, book_id):
        try:
            external_status = external_library_service.check_book_status(book_id)

            current_user = get_jwt_identity()
            print("Current user:", current_user)

            if current_user:
                status_data = {
                    "external_status": external_status,
                    "last_checked": "now()",
                }
                library_adapter.update_book_status(book_id, status_data, current_user)

            response = {"book_id": book_id, "external_libraries": external_status}
            return response, 200

        except ExternalLibraryError as e:
            return {"error": str(e)}, 503
        except LibraryServiceError as e:
            return {"error": str(e)}, 502
        except Exception:
            return {"error": "Internal Server Error"}, 500


class BookReservation(Resource):
    @jwt_required
    def post(self):
        try:
            data = request.get_json()
            if not data or "book_id" not in data:
                return {"error": "Missing book_id in request"}, 400

            current_user = get_jwt_identity()

            book_id = data["book_id"]
            user_data = data.get("user_data", {})

            external_reservation = external_library_service.reserve_book(
                book_id=book_id,
                library_id="lib1",
                user_id=user_data.get("user_id", current_user),
            )

            reservation_data = {
                "book_id": book_id,
                "external_reservation_id": external_reservation["reservation_id"],
                "external_library_id": external_reservation["library_id"],
                "status": external_reservation["status"],
                "details": {"pickup_location": "Main desk"},
            }

            result = library_adapter.create_reservation(reservation_data, current_user)
            return result, 200

        except ExternalLibraryError as e:
            return {"error": str(e)}, 503
        except LibraryServiceError as e:
            return {"error": str(e)}, 502
        except Exception as e:
            return {"error": "Internal Server Error"}, 500
