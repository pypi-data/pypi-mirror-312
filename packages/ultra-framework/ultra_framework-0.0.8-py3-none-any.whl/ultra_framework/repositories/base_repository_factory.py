from abc import ABC, abstractmethod
from typing import Self, Type, Any, Mapping

from sqlalchemy.orm import Session
from ultra_framework.repositories.crud_repository import CRUDRepository


class BaseRepositoryFactory(ABC):

    repository_map: Mapping[str, Type[CRUDRepository]]

    def __init__(self, session: Session):
        self._session = session

    @property
    def session(self) -> Session:
        return self._session

    @classmethod
    @abstractmethod
    def create_factory(cls, session: Session) -> Self: ...

    def make_repository(self, repository_name: str) -> Any:
        repository_class = self.repository_map[repository_name]
        return repository_class(self.session)
