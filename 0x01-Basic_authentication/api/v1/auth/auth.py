#!/usr/bin/env python3

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

        if path is None or not excluded_paths:
            return True

        normalized_path = path.rstrip('/')

        for excluded in excluded_paths:
            if normalized_path == excluded.rstrip('/'):
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
        return None

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
