#!/usr/bin/env python3
"""
UserSession model for storing session data in a file-based database.
"""

from models.base import Base


class UserSession(Base):
    """
    UserSession model that stores session data, including
    user_id and session_id.
    """

    def __init__(self, *args: list, **kwargs: dict):
        """
        Initialize a UserSession instance.

        Args:
            *args (list): Positional arguments.
            **kwargs (dict): Keyword arguments for initialization.
        """
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')
