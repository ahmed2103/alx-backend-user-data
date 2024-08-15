#!/usr/bin/env python3
"""DB module
"""
from typing import Dict
from sqlalchemy import create_engine, tuple_
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.session import Session

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Create a new user"""
        user = User()
        user.email = email
        user.hashed_password = hashed_password
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **attrs: Dict) -> User:
        """Find a user by attributes"""
        try:
            user = self._session.query(User).filter_by(**attrs).first()
            if user is None:
                raise NoResultFound()
            return user
        except InvalidRequestError:
            raise

    def update_user(self, user_id: int, **attrs: Dict) -> None:
        """Updates user attributes"""
        user = self.find_user_by(id=user_id)
        if user is None:
            raise NoResultFound()
            return None
        try:
            for key, value in attrs.items():
                if hasattr(user, key):
                    setattr(user, key, value)
                else:
                    raise ValueError
            self._session.commit()
        except Exception:
            self._session.rollback()
            raise
