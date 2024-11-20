#!/usr/bin/env python3
from flask import Flask, jsonify

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


if __name__ == "__main__":
    """
    Starts the Flask web server on host 0.0.0.0 and port 5000.

    This block will only execute if the script is run directly.
    The application will be accessible on the specified host and port.
    """
    app.run(host="0.0.0.0", port="5000")
