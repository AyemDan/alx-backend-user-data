#!/usr/bin/env python3
"""
Module for session-based authentication with expiration.
"""

from api.v1.auth.session_auth import SessionAuth
from datetime import datetime, timedelta
from os import getenv


class SessionExpAuth(SessionAuth):
    """
    Session authentication with expiration functionality.
    """

    def __init__(self):
        """
        Initializes the SessionExpAuth instance.
        """
        super().__init__()
        try:
            self.session_duration = int(getenv("SESSION_DURATION", 0))
        except ValueError:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """
        Creates a session with expiration.
        """
        session_id = super().create_session(user_id)
        if not session_id:
            return None

        self.user_id_by_session_id[session_id] = {
            "user_id": user_id,
            "created_at": datetime.now()
        }
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        Retrieves the user ID for a session ID with expiration check.
        """
        if session_id is None:
            return None

        session_dict = self.user_id_by_session_id.get(session_id)
        if not session_dict:
            return None

        if self.session_duration <= 0:
            return session_dict.get("user_id")

        created_at = session_dict.get("created_at")
        if not created_at:
            return None

        # Check if the session has expired
        if created_at + timedelta(
           seconds=self.session_duration) < datetime.now():
            return None

        return session_dict.get("user_id")
