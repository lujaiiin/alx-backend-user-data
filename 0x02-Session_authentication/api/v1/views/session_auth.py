#!/usr/bin/env python3
""" Modules"""

from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User
import os


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login() -> str:
    """ login"""

    email = request.form.get('email')
    if email is None or email == "":
        return jsonify({"error": "email missing"}), 400
    password = request.form.get('password')
    if password is None or password == "":
        return jsonify({"error": "password missing"}), 400
    user = User.search({'email': email})
    if len(user) == 0:
        return jsonify({"error": "no user found for this email"}), 404
    if user[0].is_valid_password(password):
        from api.v1.app import auth
        session_id = auth.create_session(user[0].id)
        response = jsonify(user[0].to_json())
        response.set_cookie(os.getenv('SESSION_NAME'), session_id)
        return response
    return jsonify({"error": "wrong password"}), 401


@app_views.route('/auth_session/logout', methods=['DELETE'],
                 strict_slashes=False)
def logout() -> str:
    """ logout"""

    from api.v1.app import auth
    if auth.destroy_session(request):
        return jsonify({}), 200
    abort(404)
