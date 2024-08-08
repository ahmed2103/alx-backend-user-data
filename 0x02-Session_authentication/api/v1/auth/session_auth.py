#!/usr/bin/env python3
"""Module for session authentication."""


from api.v1.auth.auth import Auth
import uuid
import os
from models.user import User


class SessionAuth(Auth):
    """Class for session authentication."""
    user_id_by_session_id = dict()

    def create_session(self, user_id: str = None) -> str:
        """Creates Session ID for user_id"""
        if not isinstance(user_id, str):
            return None
        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Retrieves user ID for session_id"""
        if not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """Retrieves current user from cookie"""
        session_id = self.session_cookie(request)
        if session_id:
            user_id = self.user_id_for_session_id(session_id)
            if user_id:
                return User.get(user_id)

    def destroy_session(self, request=None) -> bool:
        """Destroys session for current user"""
        sess_id = self.session_cookie(request)
        if not sess_id:
            return False
        if sess_id not in self.user_id_by_session_id:
            return False
        del self.user_id_by_session_id[sess_id]
        return True
