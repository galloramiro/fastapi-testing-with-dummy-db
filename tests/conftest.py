import pytest
from fastapi.testclient import TestClient
from sqlalchemy.exc import ProgrammingError


from src.db.database import Base
from src.main import app
from src.repositories.session import DatabaseSession
from tests.utils.testing_session import DatabaseTestingSession, engine


@pytest.fixture
def setup_database():
    """Fixture that setup the database with a
    functon socpe.
    This guaranteed an empty db for each test"""
    for table in reversed(Base.metadata.sorted_tables):
        try:
            engine.execute(table.delete())
            # Dont know how to reset the autoincrement without crashing the db
            # engine.execute(f"ALTER TABLE {table.fullname} AUTO_INCREMENT = 1;")
        except ProgrammingError:
            pass

    Base.metadata.create_all(bind=engine)


@pytest.fixture
def not_logged_client(request):
    # Override the dependencies
    app.dependency_overrides[DatabaseSession] = DatabaseTestingSession

    # Return the client with the app configured
    not_logged_client = TestClient(app)
    if request.cls is not None:
        request.cls._client = not_logged_client
    return not_logged_client


@pytest.fixture()
def testing_session():
    testing_session = DatabaseTestingSession()
    return testing_session
