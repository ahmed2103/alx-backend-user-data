#!/usr/bin/env python3
"""class for session authenication with storage safe capablity"""

from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from datetime import datetime, timedelta
class SessionDBAuth(SessionExpAuth):
    """class for session authenication with storage safe capablity"""
    def create_session(self, user_id=None):
        """Creates a new session"""
        sess_id = super().create_session(user_id)
        UserSession(session_id=sess_id, user_id=user_id).save()
        return sess_id

    def user_id_for_session_id(self, session_id=None):
        """Creates a new session"""
        try:
            user_session = UserSession.search({'session_id': session_id})[0]
        except Exception:
            return None
        created_at = user_session.created_at
        time_threshold = created_at + timedelta(seconds=self.session_duration)
        if time_threshold < datetime.now():
            return None
        return user_session.user_id

    def destroy_session(self, request=None) -> str:
        """destroys a session"""
        session_id = self.session_cookie(request)
        try:
            UserSession.search({'session_id': session_id})[0].remove()
        except Exception:
            return False
        return True






