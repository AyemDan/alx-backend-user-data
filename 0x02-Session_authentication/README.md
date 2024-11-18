# Session Authentication

This project focuses on implementing session-based authentication for a web application. The goal is to understand how to manage user sessions securely and efficiently.

## Table of Contents
- [Introduction](#introduction)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Endpoints](#endpoints)
- [License](#license)

## Introduction
Session authentication is a common method used to maintain user state across multiple requests. This project demonstrates how to create, manage, and validate user sessions.

## Requirements
- Python 3.x
- Flask
- Flask-Session
- Other dependencies listed in `requirements.txt`

## Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/alx-backend-user-data.git
    ```
2. Navigate to the project directory:
    ```bash
    cd alx-backend-user-data/0x02-Session_authentication
    ```
3. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage
1. Run the Flask application:
    ```bash
    flask run
    ```
2. Access the application at `http://127.0.0.1:5000`.

## Endpoints
- `POST /auth/login`: Logs in a user and creates a session.
- `GET /auth/logout`: Logs out a user and destroys the session.
- `GET /profile`: Retrieves the profile of the logged-in user.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.