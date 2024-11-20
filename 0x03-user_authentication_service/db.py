"""DB module
This module contains the `DB` class responsible for
interacting with the database.
It uses SQLAlchemy to handle database operations,
including user creation and session management.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
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
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object

        Returns a session object that is used for interacting
        with the database.
        If the session doesn't exist, it is created and stored.

        Returns:
        --------
        sqlalchemy.orm.Session
            The session object to interact with the database.
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
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
        self.__session.close()
        return new_user
