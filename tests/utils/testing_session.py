import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.repositories.interface import DatabaseSessionInterface

TESTING_DATABASE_URL = os.getenv("TESTING_DATABASE_URL", "sqlite:///./test.db")
engine = create_engine(
    TESTING_DATABASE_URL, connect_args=dict(check_same_thread=False)
)


class DatabaseTestingSession(DatabaseSessionInterface):
    """Manage the local session"""

    def __init__(self) -> None:
        testing_session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        self.session = testing_session()
