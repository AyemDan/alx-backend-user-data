#!/usr/bin/env python3
import os
from flask import request, jsonify, make_response
from models.user import User
from api.v1.views import app_views


@app_views.route('/auth_session/login/', methods=['POST'],
                 strict_slashes=False)
def login():
    """
    Handles user login for session authentication.
    """
    # Retrieve email and password from the form data
    email = request.form.get('email')
    password = request.form.get('password')

    if not email or email == "":
        return jsonify({"error": "email missing"}), 400
    if not password or password == "":
        return jsonify({"error": "password missing"}), 400

    users = User.search({"email": email})
    if not users or users == []:
        return jsonify({"error": "no user found for this email"}), 404
    for user in users:
        if user.is_valid_password(password):
            from api.v1.app import auth
            session_id = auth.create_session(user.id)
            resp = jsonify(user.to_json())
            session_name = os.getenv('SESSION_NAME')
            resp.set_cookie(session_name, session_id)
            return resp
    return jsonify({"error": "wrong password"}), 401


def destroy_session(self, request=None):
    """
    Deletes the user session (logs out the user).

    Args:
        request: Flask request object.

    Returns:
        bool: True if the session was successfully deleted, False otherwise.
    """
    if request is None:
        return False

    # Retrieve the session ID from the cookie
    session_id = self.session_cookie(request)
    if session_id is None:
        return False

    # Check if the session ID is linked to a User ID
    if session_id not in self.user_id_by_session_id:
        return False

    # Remove the session ID from the dictionary
    del self.user_id_by_session_id[session_id]
    return True
