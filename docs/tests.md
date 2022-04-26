# Test & Debugging

## Commands
```bash
$ pytest
$ pytest {FOLDER} -s -v 
```

## Code That Help Us Test
If you came from `Django` you will be used to `pytest-django` that make a lot of magic with the db, creating a dummy db and applying all the migrations for each test, and also restarting this db before each test.  
With `Fast-API` we dont have this advantage, but we have the injection dependency given from `Depends` that would help us on the way to.  

For this to work we have 4 basic parts:
- Dependency injection on routes
- Fixtures to share between tests
- DataBase Interface
- Repositories that use this DatabaseInterface

### Dependency injection on routes
Using the `Depends` on the database parameter of the route, we could inject the different sessions.  
You always want the regular Session, and then use the `dependency_override` to change them.  

**src/routes/route_file.py**
```python
from typing import List
from fastapi import Depends
from src.schemas import CropResponse
from src.repositories import CropRepository
from src.repositories.session import DatabaseSession, DatabaseSessionInterface

@crop_router.get("", response_model=List[CropResponse])
async def get_all(database: DatabaseSessionInterface = Depends(DatabaseSession)):
    repository = CropRepository(session=database.session)
    return repository.get_all()
```
### Fixtures To Share Between Tests
There are two important fixtures that we need:
- One fixture with Database Testing Session that connect to the dummy DB
- One fixture with a TestClient where we make the dependency override
- One fixture that set up the database


**tests/utils/testing_session.py**
```python
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
```

**tests/conftest.py**
```python
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.exc import ProgrammingError, OperationalError

from src.main import app
from src.orm import database
from src.repositories.session import DatabaseSession
from tests.utils.testing_session import DatabaseTestingSession, engine

@pytest.fixture
def setup_database():
    """Fixture that setup the database with a
    functon socpe.
    This guaranteed an empty db for each test"""
    for table in reversed(database.Base.metadata.sorted_tables):
        try:
            engine.execute(table.delete())
            # Dont know how to reset the autoincrement without crashing the db
            # engine.execute(f"ALTER TABLE {table.fullname} AUTO_INCREMENT = 1;")
        except (ProgrammingError, OperationalError):
            pass

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
```
### DataBase Interface
This interface allows us to maintain the same methods on the different sessions that we want to create.  
The context manager its important to use when you are modifying the DB to have a rollback in errors. 

**src/repositories/interface.py**
```python
from abc import ABC, abstractmethod
from contextlib import contextmanager

from src.orm.database import SessionLocal

class DatabaseSessionInterface(ABC):  # pragma: no cover
    """Allow dependency injection in the differents repositories.
    This give you the freedom to switch between local and testing
    sessions to avoid use the current db for tests.
    """

    @contextmanager
    def get_session(self):  # pragma: no cover
        """The idea of this context manager is to be used in all
        the operations that would alter the DB state, so we dont
        have session problems, and solve the rollback in case of
        an error
        """
        # we use the no cover here because we test this on the DatabaseTestingSession
        try:
            # this is where the "work" happens!
            yield self.session
            # always commit changes!
            self.session.commit()
        except:
            # if any kind of exception occurs, rollback transaction
            self.session.rollback()
            raise
        finally:
            self.session.close()
```

**src/repositories/session.py**
```python
from src.orm.database import SessionLocal
from src.repositories.interface import DatabaseSessionInterface


class DatabaseSession(DatabaseSessionInterface):
    """Manage the local session"""

    def __init__(self) -> None:
        self.session = SessionLocal()
```
### Repositories that use this DatabaseInterface
```python
from sqlalchemy.orm import Session

from src.orm.models import Crop
from src.schemas import CropRequest


class CropRepository:

    def __init__(self, session: Session):
        self.session = session

    def save(self, crop: CropRequest):
        """We strongly recomend to use this function with the
        DatabaseSession.get_session() context manager.
        Because this function will change the db.
        """
        crop = Crop(**crop.dict())
        self.session.add(crop)
        self.session.commit()
        self.session.refresh(crop)

        return crop

    def get_all(self):
        return self.session.query(Crop).all()
```