import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm.session import close_all_sessions
from sqlalchemy.exc import ProgrammingError, OperationalError


from src.orm import database
from src.main import app
from src.repositories.session import DatabaseSession
from tests.utils.testing_session import DatabaseTestingSession, engine


@pytest.fixture
def setup_database():
    """
    Fixture that setup the database with a functon socpe.
    This guaranteed an empty db for each test

    Fix to sqlalchemy freezingin drop_all:
        - https://stackoverflow.com/questions/24289808/drop-all-freezes-in-flask-with-sqlalchemy
        - https://docs.sqlalchemy.org/en/14/orm/session_api.html?highlight=close_all
    """
    close_all_sessions()
    database.Base.metadata.drop_all(bind=engine)
    database.Base.metadata.create_all(bind=engine)


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
