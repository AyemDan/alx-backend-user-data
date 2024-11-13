#!/usr/bin/env python3
""" basic_auth.py

This module provides the Basic_Auth class, which is a subclass
of the Auth class.
It is intended to handle basic authentication mechanisms for the API.

Classes:
    Basic_Auth: A subclass of Auth for basic authentication
    Currently, this class
                is empty and inherits directly from Auth.

Usage:
    This module is intended to be used as part of the
    authentication system for the API.
    The Basic_Auth class can be extended to implement
    specific basic authentication logic.

Example:

    basic_auth = Basic_Auth() """
import base64
from typing import TypeVar
from api.v1.auth.auth import Auth
from models.user import User


class BasicAuth(Auth):
    """
    BasicAuth is a subclass of Auth for handling Basic Authentication.
    """

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """
        Extracts the Base64 part of the Authorization header for
        Basic Authentication.

        Parameters:
        -----------
        authorization_header : str
            The Authorization header containing the Basic
            authentication credentials.

        Returns:
        --------
        str or None
            The Base64 part of the Authorization header if it's valid,
            otherwise returns None.
        """
        # Check if authorization_header is None or not a string
        if (authorization_header is None or
           not isinstance(authorization_header, str)):
            return None

        # Check if the header starts with "Basic "
        if not authorization_header.startswith("Basic "):
            return None

        # Return the part after "Basic "
        return authorization_header[len("Basic "):]

    def decode_base64_authorization_header(
         self, base64_authorization_header: str) -> str:
        """
        Decodes a Base64 string.

        Parameters:
        -----------
        base64_authorization_header : str
            A Base64-encoded string representing the authorization credentials.

        Returns:
        --------
        str or None
            The decoded UTF-8 string if valid, otherwise None.
        """
        # Check if base64_authorization_header is None or not a string
        if base64_authorization_header is None or not isinstance(
         base64_authorization_header, str):
            return None

        # Try to decode the Base64 string
        try:
            decoded_bytes = base64.b64decode(base64_authorization_header)
            return decoded_bytes.decode("utf-8")
        except (base64.binascii.Error, UnicodeDecodeError):
            return None

    def extract_user_credentials(
         self, decoded_base64_authorization_header: str) -> (str, str):
        """
        Extracts the user email and password from the decoded Base64 string.

        Parameters:
        -----------
        decoded_base64_authorization_header : str
            The decoded Base64 string containing user credentials.

        Returns:
        --------
        (str, str) or (None, None)
            A tuple containing the user email and password if valid,
            otherwise (None, None).
        """
        # Check if input is None or not a string
        if decoded_base64_authorization_header is None or not isinstance(
         decoded_base64_authorization_header, str):
            return None, None

        # Check if ':' is in the decoded string
        if ':' not in decoded_base64_authorization_header:
            return None, None

        # Split the string at the first occurrence of ':'
        split_header = decoded_base64_authorization_header.split(':', 1)
        if len(split_header) != 2:
            return None, None
        user_email, password = split_header[0], split_header[1]

        return user_email, password

    def user_object_from_credentials(
         self, user_email: str, password: str) -> TypeVar('User'):
        """
        Retrieves a user object based on the email and password.

        Parameters:
        -----------
        user_email : str
            The email address of the user.
        password : str
            The password of the user.

        Returns:
        --------
        TypeVar('User') or None
            A user object if the credentials are valid, otherwise None.
        """
        # Check if the email or password are None or empty
        if (user_email is None or password is None or
           not isinstance(user_email, str) or not isinstance(password, str)):
            return None

        # Check if the user exists in the database
        try:
            users = User.search({"email": user_email})
            if not users or users == []:
                return None
            for user in users:
                if user.is_valid_password(password):
                    return user
            return None
        except Exception:
            return None
