#!/usr/bin/env python3
"""Authenication module for flask api"""
from flask import request
from typing import List, TypeVar


class Auth():
    """Represents authenication to api"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """returns true if path is authorized not in excluded_paths"""
        if not path or not excluded_paths:
            return True
        path = path.rstrip('/')
        for ex_path in excluded_paths:
            ex_path = ex_path.rstrip('/')
            if path.startswith(ex_path[0:-1]) or path == ex_path:
                return False
        return True

    def authorization_header(self, request: request = None) -> str:
        """returns authorization header value"""
        if request is None or 'Authorization' not in request.headers:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """User Authorization"""
        return None
