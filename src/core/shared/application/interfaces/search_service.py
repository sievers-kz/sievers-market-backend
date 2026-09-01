from abc import ABC, abstractmethod


class ISearchService(ABC):
    @abstractmethod
    async def index_documents(self, index_name: str, documents: list[dict]) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete_documents(self, index_name: str, document_ids: list[str]) -> None:
        raise NotImplementedError

    @abstractmethod
    async def configure_index(
        self,
        index_name: str,
        index_config: dict,
    ):
        raise NotImplementedError

    @abstractmethod
    async def search(
        self,
        index_name: str,
        query: str | None = None,
        filter_expression: str | list[str] | None = None,
        page: int = 1,
        limit: int = 20,
    ):
        raise NotImplementedError
