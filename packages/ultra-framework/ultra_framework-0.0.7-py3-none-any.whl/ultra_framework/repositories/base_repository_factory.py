from abc import ABC, abstractmethod
from typing import Self, Type, Any, Mapping

from sqlalchemy.orm import Session
from ultra_framework.repositories.crud_repository import CRUDRepository


class BaseRepositoryFactory(ABC):

    def __init__(self, session: Session, repository_map: Mapping[str, Type[CRUDRepository]]):
        self._session = session
        self._repository_map = repository_map

    @property
    def session(self) -> Session:
        return self._session

    @classmethod
    @abstractmethod
    def create_factory(cls, session: Session) -> Self: ...

    def make_repository(self, repository_name: str) -> Any:
        repository_class = self._repository_map[repository_name]
        return repository_class(self.session)
