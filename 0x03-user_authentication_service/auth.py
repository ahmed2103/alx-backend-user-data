#!/usr/bin/env python3
"""Module represens Authenication system"""

import uuid
import bcrypt
from sqlalchemy.exc import NoResultFound
from db import DB
from user import User


def _hash_password(password: str) -> bytes:
    """return cypted password in bytes"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def _generate_uuid() -> str:
    """"Generate a random UUID"""
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Register a new user and saves it in the database."""
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            return self._db.add_user(email, _hash_password(password))
        raise ValueError(f'User {email} already exists')

    def valid_login(self, email: str, password: str) -> bool:
        """Validate user log in"""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False
        return bcrypt.checkpw(password.encode('utf-8'), user.hashed_password)

    def create_session(self, email: str) -> str:
        """Creates session and saves it in the database."""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return
        user.session_id = _generate_uuid()
        return user.session_id

    def get_user_from_session_id(self, session_id: str) -> User:
        """Retrieves user based on its stored session id"""
        if session_id is None:
            return None
        try:
            return self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        try:
            self._db.update_user(user_id=user_id, session_id=None)
        except Exception:
            pass
        finally:
            return None

    def get_reset_password_token(self, email: str) -> str:
        """gives token to reset password"""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError
        user.reset_token = _generate_uuid()
        return user.reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        """updates password"""
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError
        if user:
            self._db.update_user(user_id=user.id,
                                 hashed_password=_hash_password(password),
                                 reset_token=None)
