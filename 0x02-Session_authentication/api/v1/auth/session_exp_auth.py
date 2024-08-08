#!/usr/bin/env python3
"""Module to add session expiration functionality to authenication system"""


from api.v1.auth.session_auth import SessionAuth
import os
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """Class to add session expiration functionality to authenication system"""

    def __init__(self):
        """initialize the session expiration class"""
        try:
            self.session_duration = int(os.getenv('SESSION_DURATION', 0))
        except (ValueError, TypeError):
            self.session_duration = 0

    def create_session(self, user_id: str = None) -> str:
        """Create session and returns its ID"""
        sess_id = super().create_session(user_id)
        if sess_id is None:
            return None
        session_dictionary = {
            'user_id': user_id,
            'created_at': datetime.now(),
        }
        self.user_id_by_session_id[sess_id] = session_dictionary
        return sess_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Retrieves user if session_id is provided"""
        if session_id is None or session_id not in self.user_id_by_session_id:
            return None
        if self.session_duration == 0:
            return self.user_id_by_session_id[session_id].get('user_id')
        created_at = self.user_id_by_session_id[session_id].get('created_at')
        if not created_at:
            return None
        time_threshold = created_at + timedelta(seconds=self.session_duration)
        if time_threshold < datetime.now():
            return None
        return self.user_id_by_session_id[session_id].get('user_id')
