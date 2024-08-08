#!/usr/bin/env python3
"""Flask view that handles all routes for the Session authentication"""


from flask import jsonify, request, abort
from api.v1.views import app_views
from models.user import User
import os
from typing import Tuple


@app_views.route('/auth_session/login', methods=['POST'],
                 strict_slashes=False)
def auth_session_log_in() -> Tuple[str, int]:
    """logs user in"""
    email = request.form.get('email')
    if email is None:
        return jsonify({ "error": "email missing" }), 400
    password = request.form.get('password')
    if password is None:
        return jsonify({ "error": "password missing" }), 400
    try:
        user = User.search({'email': email})[0]
    except Exception:
        return jsonify({ "error": "no user found for this email" }), 404
    if not user.is_valid_password(password):
        return jsonify({ "error": "wrong password" }), 401

    from api.v1.app import auth
    sess_id = auth.create_session(user.id)
    out = jsonify(user.to_json())
    cookie_name = os.getenv('SESSION_NAME')
    out.set_cookie(cookie_name, sess_id)
    return out

@app_views.route('/auth_session/logout', methods=['DELETE'],
                 strict_slashes=False)
def auth_session_log_out() -> strTuple[str, int]:
    """logs user out"""
    from api.v1.app import auth
    if not auth.destroy_session(request):
        abort(404)
    return jsonify({}), 200