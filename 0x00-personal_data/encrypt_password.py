#!/usr/bin/env python3
"""Module to encrypt passwords"""


import bcrypt


def hash_password(password: str) -> bytes:
    """Function to encrypt passwords"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Validate password and returns True if password is valid"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
