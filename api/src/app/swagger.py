# -*- coding: utf-8 -*-
from flask import jsonify
from flask_swagger_ui import get_swaggerui_blueprint

SWAGGER_URL = "/swagger"
API_URL = "/static/swagger.json"

swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL, API_URL, config={"app_name": "Library External API"}
)


def send_swagger_json():
    return jsonify(
        {
            "swagger": "2.0",
            "info": {
                "title": "Library External API",
                "description": "API do sprawdzania statusu książek w zewnętrznych bibliotekach",
                "version": "1.0",
            },
            "basePath": "/",
            "schemes": ["http", "https"],
            "securityDefinitions": {
                "Bearer": {"type": "apiKey", "name": "Authorization", "in": "header"}
            },
            "paths": {
                "/api/v1/status/{book_id}": {
                    "get": {
                        "tags": ["books"],
                        "summary": "Sprawdź status książki",
                        "parameters": [
                            {
                                "name": "book_id",
                                "in": "path",
                                "required": True,
                                "type": "integer",
                                "description": "ID książki",
                            }
                        ],
                        "responses": {
                            "200": {
                                "description": "Status książki",
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "book_id": {"type": "integer"},
                                        "external_libraries": {
                                            "type": "array",
                                            "items": {
                                                "type": "object",
                                                "properties": {
                                                    "name": {"type": "string"},
                                                    "available": {"type": "boolean"},
                                                },
                                            },
                                        },
                                    },
                                },
                            },
                            "500": {"description": "Błąd serwera"},
                        },
                        "security": [{"Bearer": []}],
                    }
                },
                "/api/v1/reserve": {
                    "post": {
                        "tags": ["books"],
                        "summary": "Zarezerwuj książkę",
                        "parameters": [
                            {
                                "name": "body",
                                "in": "body",
                                "required": True,
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "book_id": {"type": "integer"},
                                        "user_data": {"type": "object"},
                                    },
                                },
                            }
                        ],
                        "responses": {
                            "200": {
                                "description": "Rezerwacja potwierdzona",
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "reservation_id": {"type": "string"},
                                        "status": {"type": "string"},
                                        "library_id": {"type": "string"},
                                        "details": {"type": "object"},
                                    },
                                },
                            },
                            "500": {"description": "Błąd serwera"},
                        },
                        "security": [{"Bearer": []}],
                    }
                },
            },
        }
    )
