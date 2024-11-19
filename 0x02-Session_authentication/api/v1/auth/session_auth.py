#!/usr/bin/env python3
"""
SessionAuth module for handling session-based authentication.
"""
import uuid
from api.v1.auth.auth import Auth
from models.user import User


class SessionAuth(Auth):
    """
    SessionAuth class for session-based authentication.
    """
    # Class attribute to store user_id by session_id
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        Creates a session ID for a user.

        Args:
            user_id (str): The user ID for which to create a session.

        Returns:
            str: The session ID, or None if user_id is invalid.
        """
        if user_id is None or not isinstance(user_id, str):
            return None

        # Generate a new session ID
        session_id = str(uuid.uuid4())

        # Map the session ID to the user ID
        self.user_id_by_session_id[session_id] = user_id

        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        Retrieves a user ID based on a session ID.

        Args:
            session_id (str): The session ID.

        Returns:
            str: The user ID associated with the session ID,
            or None if invalid.
        """
        if session_id is None or not isinstance(session_id, str):
            return None

        # Use .get() to safely retrieve the user ID for the session ID
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """
        Retrieves the current user based on the session cookie.
        """
        if request is None:
            return None

        # Get the session ID from the cookies
        session_id = self.session_cookie(request)

        # If no session ID is found, return None
        if session_id is None:
            return None

        # Get the user ID for the session ID
        user_id = self.user_id_for_session_id(session_id)

        # If no user ID is found, return None
        if user_id is None:
            return None

        # Retrieve the User instance from the database using the user_id
        return User.get(user_id)
