#!/usr/bin/env python3
"""
Session Authentication Routes

This module provides endpoints for user login and session management,
including session creation (login) and session destruction (logout).
"""

import os
from flask import request, jsonify, abort
from models.user import User
from api.v1.views import app_views


@app_views.route('/auth_session/login/', methods=['POST'],
                 strict_slashes=False)
def login():
    """
    Handles user login for session-based authentication.

    Endpoint:
    ---------
    POST /auth_session/login/

    Behavior:
    ---------
    - Validates email and password from the request form data.
    - Searches for a user with the provided email in the database.
    - Verifies the user's password.
    - If successful:
        - Creates a new session for the user.
        - Sets the session ID in a cookie (`SESSION_NAME`).
        - Returns the user's details in JSON format.
    - If any validation fails, an appropriate error message is returned.

    Returns:
    --------
    - 400 Bad Request: If email or password is missing.
    - 404 Not Found: If no user is found for the provided email.
    - 401 Unauthorized: If the password is incorrect.
    - 200 OK: If the user is successfully authenticated, with
    JSON user details.

    Example Request:
    ----------------
    POST /auth_session/login/
    Form Data:
    {
        "email": "user@example.com",
        "password": "securepassword"
    }

    Example Response (200):
    ------------------------
    {
        "id": "12345",
        "email": "user@example.com",
        "first_name": "John",
        "last_name": "Doe"
    }
    """
    # Retrieve email and password from the form data
    email = request.form.get('email')
    password = request.form.get('password')

    # Validate email and password
    if not email or email == "":
        return jsonify({"error": "email missing"}), 400
    if not password or password == "":
        return jsonify({"error": "password missing"}), 400

    # Search for user by email
    users = User.search({"email": email})
    if not users or users == []:
        return jsonify({"error": "no user found for this email"}), 404

    # Validate the user's password
    for user in users:
        if user.is_valid_password(password):
            from api.v1.app import auth
            # Create a session and set the session ID cookie
            session_id = auth.create_session(user.id)
            resp = jsonify(user.to_json())
            session_name = os.getenv('SESSION_NAME')
            resp.set_cookie(session_name, session_id)
            return resp

    # If no valid password is found
    return jsonify({"error": "wrong password"}), 401


@app_views.route('/auth_session/logout/', methods=['DELETE'],
                 strict_slashes=False)
def logout():
    """
    Handles user logout by destroying the session.

    Returns:
        Response: JSON response with an empty dictionary and status 200
                if the session is successfully deleted.
    """
    from api.v1.app import auth
    if auth.destroy_session(request):
        return jsonify({}), 200
    abort(404)
