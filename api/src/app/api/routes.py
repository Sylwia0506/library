# -*- coding: utf-8 -*-

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from ..schemas.book import BookStatusSchema
from ..services.external_library import ExternalLibraryService
from ..utils.decorators import cache_response

api_bp = Blueprint("api", __name__)
external_service = ExternalLibraryService()


@api_bp.route("/health")
def health_check():
    return jsonify({"status": "ok"})


@api_bp.route("/status/<int:book_id>")
@jwt_required()
@cache_response(timeout=300)
def get_book_status(book_id):
    """
    Get book availability status
    ---
    parameters:
      - name: book_id
        in: path
        type: integer
        required: true
        description: ID of the book
    responses:
      200:
        description: Book status information
        schema:
          properties:
            status:
              type: string
              example: available
    """
    try:
        schema = BookStatusSchema()
        result = external_service.check_book_status(book_id)
        return jsonify(schema.dump(result))
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@api_bp.route("/reserve", methods=["POST"])
@jwt_required()
def reserve_book():
    data = request.get_json()
    try:
        result = external_service.reserve_book(data)
        return jsonify(result)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
