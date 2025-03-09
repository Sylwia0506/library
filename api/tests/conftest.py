# -*- coding: utf-8 -*-
import os
import sys

import pytest
from app import create_app
from flask_jwt_extended import create_access_token

sys.path.append(os.path.join(os.path.dirname(__file__), "../src"))


@pytest.fixture
def app():
    os.environ["JWT_SECRET_KEY"] = "test-key"
    app = create_app()
    app.config["TESTING"] = True
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = False
    return app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def auth_headers(app):
    with app.app_context():
        access_token = create_access_token(identity="test_user")
        print("Generated token:", access_token)
        headers = {"Authorization": "Bearer {}".format(access_token)}
        print("Headers:", headers)
        return headers
