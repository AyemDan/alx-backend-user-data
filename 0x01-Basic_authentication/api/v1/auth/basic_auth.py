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
    BasicAuth is a subclass of Auth for basic authentication.
    Currently, this class is empty and inherits directly from Auth.
    """
    pass
