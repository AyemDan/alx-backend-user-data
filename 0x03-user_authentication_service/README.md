# User Authentication Service

## Description
This project is a user authentication service that provides functionalities for user registration, login, and session management. It is designed to be secure and efficient, ensuring that user data is protected.

## Features
- User registration with email and password
- User login with email and password
- Password hashing for security
- Session management with tokens
- Password reset functionality

## Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/alx-backend-user-data.git
    ```
2. Navigate to the project directory:
    ```bash
    cd alx-backend-user-data/0x03-user_authentication_service
    ```
3. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage
1. Run the application:
    ```bash
    python app.py
    ```
2. Access the service at `http://localhost:5000`.

## Endpoints
- `POST /register`: Register a new user
- `POST /login`: Login a user
- `POST /reset_password`: Reset user password
- `GET /profile`: Get user profile (requires authentication)

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request.

## License
This project is licensed under the MIT License.

## Author
Muktr
