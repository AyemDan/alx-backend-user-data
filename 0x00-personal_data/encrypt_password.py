#!/usr/bin/env python3
"""
This module provides functions to hash passwords and
verify hashed passwords using bcrypt.

Functions:
    hash_password(password: str) -> bytes:
        Hashes a password using bcrypt
        and returns the hashed password as bytes.

    is_valid(hashed_password: bytes, password: str) -> bool:
        Verifies if a given password matches the hashed password using bcrypt.
"""

import bcrypt


def hash_password(password: str) -> bytes:
    """
    Hashes a password using bcrypt.
    Args:
        password (str): The password to be hashed.
    Returns:
        bytes: The hashed password as a byte string.
    """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Check if the provided password matches the hashed password.
    Args:
        hashed_password (bytes): The hashed password to check against.
        password (str): The plain text password to verify.
    Returns:
        bool: True if the password matches the hashed password,
        False otherwise.
    """

    # Check if the password matches the hashed password
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
