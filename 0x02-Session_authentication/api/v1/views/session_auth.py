#!/usr/bin/env python3
"""
Session Authentication Routes

This module provides endpoints for user login and session management,
including session creation (login) and session destruction (logout).
"""

import os
from flask import request, jsonify, make_response
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


def destroy_session(self, request=None):
    """
    Deletes the user session (logs out the user).

    Behavior:
    ---------
    - Checks if a valid session ID is present in the request cookie.
    - If the session ID exists and is linked to a user, it removes the session.

    Args:
    -----
    request : Flask request object
        The incoming request containing the session cookie.

    Returns:
    --------
    bool:
        - True if the session was successfully deleted.
        - False if the session ID is missing, invalid, or not linked to a user.

    Example:
    --------
    - Session Cookie:
        {
            "SESSION_NAME": "session_id_123"
        }

    - Before Logout:
        user_id_by_session_id = {
            "session_id_123": "user_123"
        }

    - After Logout:
        user_id_by_session_id = {}

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
