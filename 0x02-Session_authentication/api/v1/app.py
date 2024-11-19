#!/usr/bin/env python3
"""
Route module for the API

This module sets up the API's Flask application, including routes,
authentication,
CORS settings, and error handlers. It supports multiple authentication types:
basic, session-based, and custom.
"""

from os import getenv
from api.v1.views import app_views
from api.v1.auth.auth import Auth
from api.v1.auth.basic_auth import BasicAuth
from api.v1.auth.session_auth import SessionAuth
from api.v1.auth.session_exp_auth import SessionExpAuth
from flask import Flask, jsonify, abort, request
from flask_cors import CORS

# Flask application setup
app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

# Determine authentication type based on environment variable
auth = None
AUTH_TYPE = getenv("AUTH_TYPE")
if AUTH_TYPE == "basic_auth":
    auth = BasicAuth()
elif AUTH_TYPE == "auth":
    auth = Auth()
elif AUTH_TYPE == "session_auth":
    auth = SessionAuth()
elif AUTH_TYPE == "session_exp_auth":
    auth = SessionExpAuth() 


@app.before_request
def check_authentication():
    """
    Authentication middleware that checks the authentication status
    of incoming requests.

    How it works:
    -------------
    - If `auth` is not set, all requests are allowed without checks.
    - Excluded paths (e.g., `/api/v1/status/`) do not require authentication.
    - If both the `Authorization` header and session cookie are missing, a
    401 Unauthorized is returned.
    - If the user is not authenticated (via `auth.current_user`), a 403
    Forbidden is returned.
    - If authenticated, the current user is set to `request.current_user`.

    Error Responses:
    ----------------
    - 401 Unauthorized: If authentication credentials are missing or invalid.
    - 403 Forbidden: If authentication credentials are valid but the user is
    not allowed access.
    """
    if auth is None:
        return
    if not auth.require_auth(request.path, ['/api/v1/status/',
                                            '/api/v1/unauthorized/',
                                            '/api/v1/forbidden/',
                                            '/api/v1/auth_session/login/']):
        return
    if (auth.authorization_header(request) is None and
       auth.session_cookie(request) is None):
        abort(401)
    if auth.current_user(request) is None:
        abort(403)

    request.current_user = auth.current_user(request)


@app.errorhandler(401)
def unauthorized(error) -> str:
    """
    Handles 401 Unauthorized errors by returning a JSON error message.

    Returns:
    --------
    JSON response with a 401 status code:
    {
        "error": "Unauthorized"
    }
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error) -> str:
    """
    Handles 403 Forbidden errors by returning a JSON error message.

    Returns:
    --------
    JSON response with a 403 status code:
    {
        "error": "Forbidden"
    }
    """
    return jsonify({"error": "Forbidden"}), 403


@app.errorhandler(404)
def not_found(error) -> str:
    """
    Handles 404 Not Found errors by returning a JSON error message.

    Returns:
    --------
    JSON response with a 404 status code:
    {
        "error": "Not found"
    }
    """
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    """
    Starts the Flask application.

    Host and port are determined by environment variables:
    - API_HOST (default: 0.0.0.0)
    - API_PORT (default: 5000)

    Example:
    --------
    To run the application locally:
    $ export API_HOST=127.0.0.1
    $ export API_PORT=8080
    $ python3 app.py
    """
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
