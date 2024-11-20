#!/usr/bin/env python3
from flask import Flask, jsonify, request
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
        return jsonify({"message": "Missing email or password"}), 400

    try:
        # Try to register the user via the Auth object
        user = AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"}), 201

    except Exception as e:
        # Catch the exception if the email is already registered
        return jsonify({"message": "email already registered"}), 400


if __name__ == "__main__":
    """
    Starts the Flask web server on host 0.0.0.0 and port 5000.

    This block will only execute if the script is run directly.
    The application will be accessible on the specified host and port.
    """
    app.run(host="0.0.0.0", port="5000")
