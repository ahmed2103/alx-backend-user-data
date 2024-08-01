#!/usr/bin/env python3
"""Module to encrypt passwords"""


from bcrypt import hashpw, gensalt, checkpw


def hash_password(password: str) -> bytes:
    """Function to encrypt passwords"""
    return hashpw(password.encode(), gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Validate password and returns True if password is valid"""
    return checkpw(password.encode(), hashed_password)
