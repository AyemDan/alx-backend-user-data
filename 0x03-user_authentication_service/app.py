#!/usr/bin/env python3
"""Flaskapp

Returns:
    runscode : blahblah blah
"""
from flask import Flask, jsonify, request, abort, make_response, redirect
from sqlalchemy.orm.exc import NoResultFound
from auth import Auth


AUTH = Auth()

app = Flask(__name__)


@app.route("/", methods=["GET"])
def home():
    """
    Home route handler that returns a simple welcome message.

    This route is triggered by a GET request to the root URL ("/").
    It returns a JSON response containing a welcome message.

    Returns:
    -------
    Response
        A JSON response with a key "message" and value "Bienvenue".

    Example:
    --------
    >>> GET /
    HTTP/1.1 200 OK
    Content-Type: application/json
    {
        "message": "Bienvenue"
    }
    """
    payload = {"message": "Bienvenue"}

    return jsonify(payload)


@app.route('/users', methods=['POST'])
def register_user():
    """
    Registers a new user by accepting an email and password
    through a POST request.

    This route allows the creation of a new user. It expects form data
    containing an email and password. The user is registered using the
    Auth object's `register_user` method.

    Parameters:
    -----------
    email : str
        The email address of the user to register. Must be
        provided in the form data.
    password : str
        The password for the user. Must be provided in the form data.

    Returns:
    --------
    Response
        A JSON response with a status message and an
        appropriate HTTP status code.

    Responses:
    ----------
    - If both email and password are provided and the user
    is created successfully:
      - JSON: {"email": email, "message": "user created"}
      - Status code: 201 (Created)

    - If either email or password is missing:
      - JSON: {"message": "Missing email or password"}
      - Status code: 400 (Bad Request)

    - If the email is already registered:
      - JSON: {"message": "email already registered"}
      - Status code: 400 (Bad Request)

    Example:
    --------
    POST /users
    Content-Type: application/x-www-form-urlencoded
    email=example@example.com&password=securepassword

    Response:
    {
        "email": "example@example.com",
        "message": "user created"
    }
    HTTP/1.1 201 Created
    """
    # Get the form data (email and password)
    email = request.form.get('email')
    password = request.form.get('password')

    # Check if both email and password are provided
    if not email or not password:
        abort(400, description="Email and password are required")

    try:
        # Attempt to register the user (this will check if the user exists)
        user = AUTH.register_user(email, password)
        # If registration is successful, return the success message
        return jsonify({
            "email": user.email,
            "message": "user created"
        })
    except Exception as e:
        # If user already exists (or other exception), handle it
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'])
def login():
    """
    Login function to create a session for the user.

    Handles user login by validating the provided email and password.
    If the credentials are valid, a session is created, and a session
    ID is stored as a cookie in the response.

    Steps:
    ------
    1. Extract the email and password from the request form data.
    2. Validate the user's credentials using the Auth service.
    3. If valid, create a session and return the session ID as a cookie.

    Returns:
    --------
    Response:
        A JSON response with the user's email and a success message if
        login is successful.
        Sets a "session_id" cookie with the session ID.
        Returns 401 if the email or password is missing, invalid, or not found.
    """
    email = request.form.get('email')
    password = request.form.get('password')

    if not email or not password:
        abort(401)

    try:
        user = AUTH._db.find_user_by(email=email)
        if user:
            if not AUTH.valid_login(email, password):
                abort(401)
        print(user)
    except NoResultFound:
        # Handle user not found error
        abort(401, description="User not found")

    # Step 3: Create a session for the user
    session_id = AUTH.create_session(email)

    # Step 4: Set session ID as a cookie in the response
    response = make_response(jsonify({"email": email, "message": "logged in"}))
    response.set_cookie("session_id", session_id)

    return response


@app.route('/sessions', methods=['DELETE'])
def logout():
    """
    Handles the DELETE /sessions route to log out a user by
    invalidating their session.

    Workflow:
    ---------
    1. Retrieve the session ID from cookies.
    2. Verify that the session ID exists.
    3. Look up the user associated with the session ID.
    4. If the session ID is invalid or no user is associated,
    respond with a 403 status code.
    5. If valid, destroy the user's session.
    6. Redirect the user to the homepage.

    Returns:
    --------
    - A 403 error if the session ID is missing or invalid.
    - A redirect to the homepage (`/`) upon successful logout.
    """
    # Step 1: Retrieve session ID from cookies
    session_id = request.cookies.get("session_id")

    # Step 2: Check if the session ID is missing
    if session_id is None:
        # Respond with 403 Forbidden if session_id is not present
        abort(403)

    # Step 3: Look up the user associated with the session ID
    user = AUTH.get_user_from_session_id(session_id)

    # Step 4: Check if the session ID is invalid or user is not found
    if user is None:
        # Respond with 403 Forbidden if no user is linked to the session_id
        abort(403)

    # Step 5: Destroy the session associated with the user
    AUTH.destroy_session(user.id)

    # Step 6: Redirect the user to the homepage
    return redirect('/')


@app.route('/profile', methods=['GET'])
def profile():
    """
    Handle GET /profile route to return user email.
    """
    # Retrieve session_id from cookies
    session_id = request.cookies.get("session_id")

    if session_id is None:
        # Respond with 403 if session_id is missing
        abort(403)

    # Find the user with the given session_id
    user = AUTH.get_user_from_session_id(session_id)

    if user is None:
        # Respond with 403 if no user is found
        abort(403)

    # Respond with the user's email
    return jsonify({"email": user.email}), 200


@app.route('/reset_password', methods=['POST'])
def get_reset_password_token():
    """
    Generates a reset password token for a given email address.
    This function retrieves the email address from the request form data,
    validates its presence, and then attempts to generate a reset password
    token using the AUTH service. If the email is not provided or if the
    token generation fails, it aborts the request with a 403 status code.
    Returns:
        Response: A JSON response containing the email and the reset token.
    Raises:
        403: If the email is not provided or if the token generation fails.
    """
    email = request.form.get('email')
    if not email:
        abort(403)

    try:
        token = AUTH.get_reset_password_token(email)
    except ValueError:
        abort(403)

    return jsonify({"email": email, "reset_token": token})


@app.route('/reset_password', methods=['PUT'])
def update_password():
    """
    Update the user's password using a reset token.
    This function retrieves the email, new password, and reset token from the
    request form. It validates the presence of these fields and attempts to
    update the password using the provided reset token. If the reset token is
    invalid, it aborts with a 403 status code.
    Returns:
        Response: A JSON response containing the email and a success message
                  with a 200 status code if the password is
                  updated successfully.
    Raises:
        HTTPException: If any of the required fields
        (email, new_password, reset_token)
                       are missing, it aborts with a 400 status code.
        HTTPException: If the reset token is invalid,
        it aborts with a 403 status code.
    """
    email = request.form.get('email')
    new_password = request.form.get('new_password')
    reset_token = request.form.get('reset_token')

    if not email or not reset_token or not new_password:
        abort(400, description="Missing required fields")

    try:
        AUTH.update_password(reset_token, new_password)
    except ValueError:
        abort(403, description="Invalid reset token")

    return jsonify({"email": email, "message": "Password updated"}), 200


if __name__ == "__main__":
    """
    Starts the Flask web server on host 0.0.0.0 and port 5000.

    This block will only execute if the script is run directly.
    The application will be accessible on the specified host and port.
    """
    app.run(host="0.0.0.0", port="5000")
