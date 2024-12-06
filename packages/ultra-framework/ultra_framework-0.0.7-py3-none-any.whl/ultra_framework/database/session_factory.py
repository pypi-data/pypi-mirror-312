"""session_factory module"""
from typing import Iterator

from sqlalchemy.orm import sessionmaker, Session


class SessionFactory:
    """SessionFactory class"""

    def __init__(self, session_maker: sessionmaker):
        self._session_maker = session_maker

    def create_session(self) -> Iterator[Session]:
        """creates a session object from the session maker"""
        session = self._session_maker()

        try:
            yield session
        finally:
            session.close()
