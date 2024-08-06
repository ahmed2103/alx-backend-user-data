#!/usr/bin/env python3
"""Basic authincation module"""
import binascii
from api.v1.auth.auth import Auth
import base64
from models.user import User
from flask import request
from typing import TypeVar, Tuple

class BasicAuth(Auth):
    """Authenication Class for Flask API using Basic Auth"""

    def extract_base64_authorization_header(self,
                                            authorization_header: str
                                            ) -> str:
        """Returns the Base64 part of the Authorization header
            for a Basic Authentication"""
        if (not authorization_header or
                not isinstance(authorization_header, str)):
            return None
        if authorization_header.startswith('Basic '):
            return authorization_header[6:]

    def decode_base64_authorization_header(self,
                                           base64_authorization_header: str
                                           ) -> str:
        """Returns the decoded value of a Base64 string"""
        if (not base64_authorization_header or
            not isinstance(base64_authorization_header, str)):
            return None
        try:
            return (base64.b64decode(base64_authorization_header).
                    decode('utf-8'))
        except (binascii.Error, UnicodeDecodeError):
            return None

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header: str
                                 ) -> Tuple[str, str]:
        """extracts the username and password from a formatted string"""
        try:
            username, password = (
                decoded_base64_authorization_header.split(':', 1))
            return username, password
        except (AttributeError, ValueError):
            return None, None

    def user_object_from_credentials(self, user_email: str,
                                     user_pwd: str
                                     ) -> TypeVar('User'):
        """Returns a User object from a username and password"""
        if not user_email or not user_pwd:
            return None
        if not User.all():
            return None
        try:
            user = User.search({'email': user_email})[0]
        except IndexError:
            return None
        if not user.is_valid_password(user_pwd):
            return None
        return user

    def current_user(self, request: request = None) -> TypeVar('User'):
        """Returns a User based on request header"""
        auth_header = self.authorization_header(request)
        if auth_header:
            base64_auth = (
                self.extract_base64_authorization_header(auth_header))
            if base64_auth:
                decoded_auth = (
                    self.decode_base64_authorization_header(base64_auth))
                if decoded_auth:
                    email, pwd = self.extract_user_credentials(decoded_auth)
                    if email and pwd:
                        return self.user_object_from_credentials(email, pwd)
        return None
