from abc import ABC, abstractmethod
from typing import Self, Type

from sqlalchemy.orm import Session
from ultra_framework.repositories.crud_repository import CRUDRepository


class BaseRepositoryFactory(ABC):

    def __init__(self, session: Session):
        self._session = session

    @property
    def session(self) -> Session:
        return self._session

    @classmethod
    @abstractmethod
    def create_factory(cls, session: Session) -> Self: ...

    def make_repository[T](self, repository_class: Type[CRUDRepository[T]]) -> CRUDRepository[T]:
        return repository_class(self.session)
