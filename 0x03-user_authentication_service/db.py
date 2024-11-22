#!/usr/bin/env python3
"""DB module
This module contains the `DB` class responsible for
interacting with the database.
It uses SQLAlchemy to handle database operations,
including user creation and session management.
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm import scoped_session

from user import Base, User


class DB:
    """
    DB class

    The `DB` class handles database operations, including
    establishing a connection
    to the database and interacting with the `users` table.
    It uses SQLAlchemy ORM
    to add new users and manage database sessions.

    Attributes:
    -----------
    _engine : sqlalchemy.engine.Engine
        The engine used to connect to the SQLite database.

    __session : sqlalchemy.orm.Session
        The session object used to interact with the database.

    Methods:
    --------
    _session : sqlalchemy.orm.Session
        A memoized session object to interact with the database.

    add_user(email: str, hashed_password: str) -> User
        Adds a new user to the database with the given
        email and hashed password.
    """

    def __init__(self) -> None:
        """Initialize a new DB instance

        Initializes the SQLite engine, creates the database schema
        (or drops it and
        recreates it), and sets up a session.
        """
        self._engine = create_engine("sqlite:///a.db",
                                     echo=False,
                                     connect_args={"check_same_thread": False})
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """
        Creates and returns a new SQLAlchemy session if one
        does not already exist.
        This method checks if a session has already been
        created. If not, it creates
        a new session using a scoped session factory bound
        to the engine. The session
        is then stored in the instance variable `__session` and returned.
        Returns:
            Session: An SQLAlchemy session object.
        """
        if self.__session is None:
            DBSession = scoped_session(sessionmaker(bind=self._engine))
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Add a new user to the database

        Creates a new user record in the database with the given
        email and hashed password.

        Parameters:
        -----------
        email : str
            The email of the user to be added.

        hashed_password : str
            The hashed password of the user to be added.

        Returns:
        --------
        User
            The newly created user object.

        Closes the session after committing the transaction.
        """
        new_user = User(email=email, hashed_password=hashed_password)
        self._session.add(new_user)
        self._session.commit()
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """Find a user by the given keyword arguments

        Searches for a user in the database based on the
        provided keyword arguments.

        Parameters:
        -----------
        **kwargs
            Arbitrary keyword arguments to filter the user by.

        Returns:
        --------
        User
            The user object that matches the provided filters.

        Closes the session after the query is executed.
        """
        all_users = self._session.query(User)
        for k, v in kwargs.items():
            if k not in User.__dict__:
                raise InvalidRequestError
            for usr in all_users:
                if getattr(usr, k) == v:
                    return usr
        raise NoResultFound

    def update_user(self, user_id: int, **kwargs) -> None:
        """
        Updates the attributes of a user in the database.

        This method retrieves a user by their ID and updates
        specified attributes
        using the keyword arguments passed to the method.
        It raises a ValueError if
        an invalid attribute name is provided.

        Parameters:
        -----------
        user_id : Integer
            The ID of the user to be updated.

        **kwargs : dict
            Arbitrary keyword arguments where each key is the attribute name
            to be updated and the value is the new value for that attribute.

        Returns:
        --------
        None
            This method does not return any value. It performs
            the update in-place
            in the database.

        Raises:
        -------
        ValueError
            If any attribute name in **kwargs does not exist on the User model.
        """
        user = self.find_user_by(id=user_id)
        for k, value in kwargs.items():
            if not hasattr(User, k):
                raise ValueError
            setattr(user, k, value)
            self.__session.add(user)
            self._session.commit()

        return None
