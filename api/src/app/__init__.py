# -*- coding: utf-8 -*-
from __future__ import print_function

import os

from dotenv import load_dotenv
from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_restful import Api
from flask_swagger_ui import get_swaggerui_blueprint


def create_app():
    load_dotenv()

    app = Flask(__name__)
    api = Api(app)

    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "your-secret-key-here")
    jwt = JWTManager(app)

    @jwt.invalid_token_loader
    def invalid_token_callback(error_string):
        return jsonify({"error": "Invalid token", "description": error_string}), 401

    @jwt.unauthorized_loader
    def unauthorized_callback(error_string):
        return jsonify({"error": "No token provided", "description": error_string}), 401

    @jwt.expired_token_loader
    def expired_token_callback():
        return (
            jsonify(
                {
                    "error": "Token has expired",
                    "description": "Please refresh your token",
                }
            ),
            401,
        )

    SWAGGER_URL = "/swagger"
    API_URL = "/static/swagger.json"

    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL, API_URL, config={"app_name": "Library External API"}
    )
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

    from app.swagger import send_swagger_json
    from app.views import BookReservation, BookStatus

    api.add_resource(BookStatus, "/api/v1/status/<int:book_id>")
    api.add_resource(BookReservation, "/api/v1/reserve")
    app.add_url_rule("/static/swagger.json", "swagger_json", send_swagger_json)

    return app


app = create_app()
