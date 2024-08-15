#!/usr/bin/env python3
"""Basic Flask app."""
from http.client import responses
from typing import Tuple
from flask import Flask, request, jsonify, abort, redirect
from auth import Auth

auth = Auth()
app = Flask(__name__)

@app.route("/", strict_slashes=False)
def index() -> str:
    """GET /
        Returns a JSON payload of the form"""
    return jsonify({ "message": "Bienvenue" })

@app.route("/users", methods=["POST"], strict_slashes=False)
def user_registration()-> Tuple[str, int]:
    """POST /users
        Register a new user"""
    data = request.form
    if 'email' in data and 'password' in data:
        try:
            auth.register_user(email = data['email'], password = data['password'])
            return jsonify({'email': data['email'],
                            "message": "user created"}
                           ),200
        except ValueError:
            return jsonify({"message": "email already registered"}), 400

@app.route("/sessions", methods=["POST"], strict_slashes=False)
def login_session()-> Tuple[str, int]:
    """POST /sessions
        logs user in"""
    email = request.form.get('email')
    password = request.form.get('password')
    if email and password:
        if auth.valid_login(email, password):
            session_id = auth.create_session(email)
            res = jsonify({"email": f"{email}", "message": "logged in"})
            res.set_cookie("session_id", session_id)
            return res, 200
    abort(401)

@app.route("/sessions", methods=["DELETE"], strict_slashes=False)
def logout_session()-> Tuple[str, int]:
    """DELETE /sessions
    logs user out"""
    session_id = request.cookies.get("session_id")
    if session_id:
        user = auth.get_user_from_session_id(session_id)
        auth.destroy_session(user.id)
        return redirect('/')

@app.route("/profile", strict_slashes=False)
def user_profile()-> Tuple[str, int]:
    """GET /profile
        returns user profile in json"""
    session_id = request.cookies.get("session_id")
    user = auth.get_user_from_session_id(session_id)
    if user:
        return jsonify({'email': user.email}), 200
    else:
        abort(403)

@app.route('/reset_password', methods=["POST"], strict_slashes=False)
def reset_password()-> Tuple[str, int]:
    """POST /reset_password
        rturns reset token"""
    email = request.form.get('email')
    try:
        reset_tokent = auth.get_reset_password_token(email)
    except ValueError:
        abort(403)
    return jsonify({'email': email, 'reset_token': reset_tokent}), 200

@app.route('/reset_password', methods=["PUT"], strict_slashes=False)
def update_passwoed()-> Tuple[str, int]:
    """PUT /reset_password
        updates user password"""
    email = request.form.get('email')
    password = request.form.get('password')
    reset_tokent = request.form.get('reset_token')
    if email and password and reset_tokent:
        try:
            auth.update_password(reset_tokent, password)
            return jsonify({'email':email,"message":"Password updated"}), 200
        except ValueError:
            abort(403)




if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")