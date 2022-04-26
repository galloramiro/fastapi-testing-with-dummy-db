from src.orm.database import SessionLocal
from src.repositories.interface import DatabaseSessionInterface


class DatabaseSession(DatabaseSessionInterface):
    """Manage the local session"""

    def __init__(self) -> None:
        self.session = SessionLocal()
