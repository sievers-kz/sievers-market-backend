from abc import ABC, abstractmethod

from src.core.catalog.application.interfaces import (
    ICategoryRepository,
    IRubricRepository,
    ISubcategoryRepository,
)


class ICatalogUnitOfWork(ABC):
    @property
    @abstractmethod
    def rubric(self) -> IRubricRepository:
        raise NotImplementedError

    @property
    @abstractmethod
    def category(self) -> ICategoryRepository:
        raise NotImplementedError

    @property
    @abstractmethod
    def subcategory(self) -> ISubcategoryRepository:
        raise NotImplementedError
