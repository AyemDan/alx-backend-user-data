#!/usr/bin/env python3

'''This module provides the `Auth` class, which defines methods for handling
authentication-related tasks in a web application. It includes methods to
check if authentication is required for a given path, retrieve an
authorization header from a request, and get the current user based on the
request.

Classes:
Auth:
    A class that provides methods for authentication-related tasks.'''


from os import getenv
from typing import List, TypeVar
from flask import request, jsonify, make_response


class Auth:
    """
    This class defines methods for handling authentication-related tasks in a
    web application.
    It provides methods to check if authentication is required,
    retrieve an authorization header,
    and get the current user from the request.

    Methods:
    --------
    require_auth(path: str, excluded_paths: List[str]) -> bool:
        Determines if authentication is required for the given path.

    authorization_header(request=None) -> str:
        Retrieves the authorization header from the request.

    current_user(request=None) -> TypeVar('User'):
        Retrieves the current user based on the request. This
        is usually determined by the
        authorization header or session information.
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Determines if authentication is required for the given path.

        Parameters:
        -----------
        path : str
            The path to check for authentication requirement.
        excluded_paths : List[str]
            A list of paths that do not require authentication.

        Returns:
        --------
        bool
            Returns True if authentication is required for the given path,
            False if the path is in the excluded_paths list.
        """

        if path is None or excluded_paths is None or len(excluded_paths) == 0:
            return True

        normalized_path = path.rstrip('/')

        for excluded in excluded_paths:
            # Handle wildcard at the end of the excluded path
            if excluded.endswith('*'):
                # Check if path starts with the excluded path prefix
                if normalized_path.startswith(excluded.rstrip('*')):
                    return False
            # Handle exact matches
            elif normalized_path == excluded.rstrip('/'):
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """
        Retrieves the authorization header from the request.

        Parameters:
        -----------
        request : Flask Request, optional
            The HTTP request object, which may contain an authorization header.

        Returns:
        --------
        str
            Returns None as the default authorization header,
            indicating no header is present.
        """
        if (request is None or request.headers is None
           or 'Authorization' not in request.headers):
            return None

        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Retrieves the current user based on the request.

        Parameters:
        -----------
        request : Flask Request, optional
            The HTTP request object, which may contain user
            identification information.

        Returns:
        --------
        TypeVar('User')
            Returns None as a placeholder for the current user,
            indicating no user is set.
        """
        return None

    def session_cookie(self, request=None):
        """
        Retrieves the session ID from the cookies of the request.

        Args:
            request (flask.Request): The request object.

        Returns:
            str: The session ID, or None if the request is invalid
            or cookie not found.
        """
        if request is None:
            return None

        # Get the name of the session cookie from the environment variable
        session_name = getenv("SESSION_NAME")

        # Use .get() to safely retrieve the cookie value by the session name
        return request.cookies.get(session_name)
