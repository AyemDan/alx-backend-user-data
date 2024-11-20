#!/usr/bin/env python3
"""
User Model Definition

This module defines the `User` class, which represents a user in the database.
It uses SQLAlchemy's ORM to map the `users` table to the `User` Python class.
"""

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

# Base class for SQLAlchemy models
Base = declarative_base()


class User(Base):
    """
    User Model

    Represents the `users` table in the database, storing user details
    including their email, hashed password, session ID, and reset token.

    Attributes:
    -----------
    __tablename__ : str
        The name of the table in the database (`users`).

    id : int
        The primary key of the user record.

    email : str
        The user's email address, must not be null.

    hashed_password : str
        The hashed version of the user's password, must not be null.

    session_id : str, optional
        An optional field to store the session ID for the user.

    reset_token : str, optional
        An optional field to store the password reset token for the user.
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    session_id = Column(String, nullable=True)
    reset_token = Column(String, nullable=True)
