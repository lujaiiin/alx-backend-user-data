#!/usr/bin/env python3
"""modules"""
import bcrypt


def hash_password(password: str) -> bytes:
    """fun"""

    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """fun"""

    return bcrypt.checkpw(password.encode(), hashed_password)
