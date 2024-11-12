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

from api.v1.auth.auth import Auth


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
