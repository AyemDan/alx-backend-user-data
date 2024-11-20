#!/usr/bin/env python3
import uuid
import bcrypt
from db import DB
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """
    Hashes a password with a salt using bcrypt.

    This function generates a salt and uses bcrypt to hash
    the provided password
    with the generated salt. The result is a salted hash of
    the password that can
    be securely stored.

    Parameters:
    ----------
    password : str
        The password string to hash.

    Returns:
    -------
    bytes
        The salted bcrypt hash of the password.

    Example:
    --------
    >>> _hash_password("my_secure_password")
    b"$2b$12$k1zTb5T6uK1bPwrEZYfgP6X60XvWV/oc9.cxx8HE9DffVwOshe13W"
    """
    # Generate a salt
    salt = bcrypt.gensalt()

    # Hash the password with the salt
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

    return hashed_password


class Auth:
    """Auth class to interact with the authentication database.

    This class handles user registration, authentication,
    and password management.
    It interfaces with the database through the DB class to add new users, find
    existing users, and hash passwords for secure storage.
    """

    def __init__(self):
        """
        Initializes the Auth class and sets up the database instance.

        The constructor initializes the database connection using the DB class,
        which is responsible for handling user data and performing
        CRUD operations.
        """
        self._db = DB()

    def register_user(self, email: str, password: str):
        """
        Registers a new user by adding their email and hashed password
        to the database.

        The method first checks if a user with the given email already exists.
        If the email is not found, it hashes the provided password and adds the
        new user to the database. If the user already exists,
        it raises a ValueError.

        Parameters:
        ----------
        email : str
            The email of the user to register.

        password : str
            The password for the new user, which will be hashed before storage.

        Returns:
        -------
        usr : User
            The newly created user object added to the database.

        Raises:
        -------
        ValueError
            If a user with the provided email already exists.

        Example:
        --------
        >>> auth = Auth()
        >>> auth.register_user("example@test.com", "my_secure_password")
        User object
        """
        try:
            # Check if the user already exists
            self._db.find_user_by(email=email)
        except NoResultFound:
            # If user does not exist, hash the password and add the user
            hashed = _hash_password(password)
            usr = self._db.add_user(email, hashed)
            return usr
        raise ValueError(f"User {email} already exists")

    def valid_login(self, email, password) -> bool:
        """
        Validates the login credentials (email and password) against the
        stored user data.

        This method checks if the provided email exists in the database,
        and if it does,
        it verifies if the provided password matches the stored
        hashed password.

        Parameters:
        -----------
        email : str
            The email of the user trying to log in.

        password : str
            The password provided by the user attempting to log in.

        Returns:
        --------
        bool
            Returns True if the email exists in the database and
            the provided password
            matches the stored hashed password. Returns False if
            either the email doesn't
            exist or the password is incorrect.

        Exceptions:
        -----------
        NoResultFound:
            If the provided email does not match any user in the database.

        Example:
        --------
        >>> auth.valid_login("user@example.com", "securepassword")
        True

        >>> auth.valid_login("user@example.com", "wrongpassword")
        False

        >>> auth.valid_login("nonexistent@example.com", "password")
        False
        """
        try:
            user = self._db.find_user_by(email=email)
            if user:
                return bcrypt.checkpw(
                    password.encode('utf-8'), user.hashed_password)
        except NoResultFound:
            return False

    def _generate_uuid(self) -> str:
        """
        Generate and return a new UUID (Universally Unique Identifier)
        as a string.

        This method uses the `uuid` module to generate a random
        UUID and returns it as a string.

        Returns:
        --------
        str
            A string representation of a newly generated UUID.

        Example:
        --------
        >>> _generate_uuid()
        '123e4567-e89b-12d3-a456-426614174000'

        Notes:
        ------
        - This UUID is generated using the `uuid4()` method,
        which produces a random UUID.
        - The generated UUID will be unique with a very high
        probability.
        """
        return str(uuid.uuid4())
