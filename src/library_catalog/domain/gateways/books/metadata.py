from abc import abstractmethod
from typing import Protocol

from src.library_catalog.domain.vo.books import BookMetadata


class BookMetadataGatewayProtocol(Protocol):
    @abstractmethod
    async def fetch_metadata(self, name: str, author: str) -> BookMetadata | None: ...
