from sqlalchemy.orm import Session


def test_testing_session_have_session(testing_session):
    assert isinstance(testing_session.session, Session)


def test_testing_session_have_interface_get_session_method(testing_session):
    with testing_session.get_session() as session:
        assert isinstance(session, Session)
