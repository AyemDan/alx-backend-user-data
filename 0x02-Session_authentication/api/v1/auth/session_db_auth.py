#!/usr/bin/env python3
"""
Session-based authentication with database persistence.
"""

from datetime import datetime, timedelta
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """
    SessionDBAuth stores session data in the database using UserSession model.
    """

    def create_session(self, user_id=None):
        """
        Create a session and store it in the database.

        Args:
            user_id (str): The ID of the user.

        Returns:
            str: The created session ID.
        """
        if not user_id:
            return None

        session_id = super().create_session(user_id)
        if not session_id:
            return None

        user_session = UserSession(user_id=user_id, session_id=session_id)
        if user_session:
            user_session.save()  # Save to the database
            return session_id

        return

    def user_id_for_session_id(self, session_id=None):
        """
        Retrieve the user ID for a given session ID from the database.

        Args:
            session_id (str): The session ID.

        Returns:
            str: The user ID or None if not found.
        """
        if not session_id:
            return None

        user_sessions = UserSession.search({'session_id': session_id})
        if not user_sessions:
            return None

        user_session = user_sessions[0]
        if self.session_duration <= 0:
            return user_session.user_id

        created_at = user_session.created_at
        if not created_at:
            return None

        if created_at + timedelta(
           seconds=self.session_duration) < datetime.now():
            user_session.remove()  # Remove expired session
            return user_session.user_id

        return None

    def destroy_session(self, request=None):
        """
        Destroy a session by removing it from the database.

        Args:
            request: The Flask request object.

        Returns:
            bool: True if the session was destroyed, False otherwise.
        """
        if not request:
            return False

        session_id = self.session_cookie(request)
        if not session_id:
            return False

        user_sessions = UserSession.search({'session_id': session_id})
        if not user_sessions:
            return False

        user_session = user_sessions[0]
        user_session.remove()  # Remove from the database
        return True
