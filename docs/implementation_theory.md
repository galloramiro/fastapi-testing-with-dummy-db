# Test & Debugging

## Summary
- [Why did we do this](#why-did-we-do-this)
- [Core concepts](#core-concepts)
  - [Interfaces](#interfaces)
  - [Repository Pattern](#repository-pattern)
  - [Dependency Injection](#dependency-injection)
- [Code examples and explanation](#code-examples-and-explanation)
  - [Dependency injection on routes](#dependency-injection-on-routes)
  - [Fixtures to share between tests](#fixtures-to-share-between-tests)
  - [DataBase interface](#database-interface)
  - [Repositories that use this DatabaseInterface](#repositories-that-use-this-databaseinterface)

## Why did we do this
If you came from `Django` you will be used to `pytest-django` that make a lot of magic with the db, creating a dummy db and applying all the migrations for each test, and also restarting this db before each test.  
Having the opportunity to use a prod like database in your tests is important if you have complex queries, or logic depending on different operations on your project.  
Otherwise, you are having the risk of supposing some things works, and you learn in production that they don't... hahaha  
With `Fast-API` we don't have this advantage, but we have the injection dependency given from `Depends` that would help us on the way to.  

## Core concepts
This would be a simple overview of the concepts. For more in depth knowledge I recommend reed the links that I live you in each concept.

### Interfaces
The interface is like a contract that we make in order to ensure that we are going be talking all the same language.  
In this case, we are going to use this concept in order to ensure that we are going to receive a class that have a session and a context manager function.  
This will let us change between the different databases with our breaking the contract that we have.   
Good explanation on this concept [here](https://refactoring.guru/extract-interface). 

### Repository pattern
The repository pattern is used to encapsulate database access logic.  
For example if we need to get all crops form the db and make some calculations based on climatic and other parameters we are gonna have the calculation login in one place and the query in a repository that returns the objects that we need.
In this way all the interactions that we are going make to the DB are gonna be though this classes and we could make our system independent of this, and we also can test this in a separate way.  
Good explanation on this concept [here](https://docs.microsoft.com/en-us/dotnet/architecture/microservices/microservice-ddd-cqrs-patterns/infrastructure-persistence-layer-design). 

### Dependency injection
The dependency injection allows you to switch entire objects into your classes generating more cohesion, in this case switch between the `Database` and the `TestingDatabase`.
Also, FastApi has a class that allow you to switch dependencies on the app setup, and this will help us a lot!
Good explanation on this concept [here](https://python-dependency-injector.ets-labs.org/introduction/di_in_python.html)

## Code examples and explanation
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
### Fixtures to share between tests
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
```
### DataBase interface
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