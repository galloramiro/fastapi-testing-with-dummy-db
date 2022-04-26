from abc import ABC
from contextlib import contextmanager


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
