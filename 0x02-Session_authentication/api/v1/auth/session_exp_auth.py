#!/usr/bin/env python3
"""modules"""
import os
from api.v1.auth.session_auth import SessionAuth
import datetime

from models.user import User


class SessionAuth(SessionAuth):
    """class"""

    def __init__(self):
        """init"""

        try:
            self.session_duration = int(os.getenv('SESSION_DURATION', 0))
        except Exception:
            self.session_duration = 0

    def create_session(self, user_id: str = None) -> str:
        """func"""

        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        session_dictionary = {
            "user_id": user_id,
            "created_at": datetime.datetime.now()
        }
        self.user_id_by_session_id[session_id] = session_dictionary
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """fun"""

        session_dictionary = super().user_id_for_session_id(session_id)
        if session_dictionary is None:
            return None
        created_at = session_dictionary.get("created_at")
        if created_at is None:
            return None
        user_id = session_dictionary.get("user_id")
        if self.session_duration <= 0:
            return user_id
        now = datetime.datetime.now()
        duration = datetime.timedelta(seconds=self.session_duration)
        if now > created_at + duration:
            return None
        return user_id
