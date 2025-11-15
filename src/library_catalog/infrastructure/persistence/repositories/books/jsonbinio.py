from __future__ import annotations

import asyncio
from datetime import UTC, datetime
from uuid import UUID  # noqa: TC003

from src.library_catalog.domain.entities.books import BookEntity
from src.library_catalog.domain.exceptions.books import BookAlreadyExistsException
from src.library_catalog.domain.repositories.books import BookRepositoryProtocol
from src.library_catalog.domain.vo.books import BookFilters, PaginationSpec, QueryResult, SortSpec
from src.library_catalog.infrastructure.http.clients.aiohttp import AioHttpClient
from src.library_catalog.infrastructure.persistence.mappers.books import dict_to_domain, domain_to_json_dict


class BooksRepositoryJsonbinioImpl(BookRepositoryProtocol):
    BASE_URL = "https://api.jsonbin.io/v3"

    def __init__(self, api_key: str, bin_id: str | None = None):
        self.api_key = api_key
        self.bin_id = bin_id
        self._write_lock = asyncio.Lock()

    def _get_headers(self) -> dict[str, str]:
        return {
            "X-Master-Key": self.api_key,
        }

    async def _read_data(self) -> list[dict]:
        if not self.bin_id:
            return []

        async with AioHttpClient() as client:
            response = await client.get(
                f"{self.BASE_URL}/b/{self.bin_id}/latest",
                headers=self._get_headers(),
            )
            if response.status_code >= 400:
                return []
            return response.data.get("record", []) if isinstance(response.data, dict) else []

    async def _write_data(self, data: list[dict]) -> None:
        async with AioHttpClient() as client:
            if not self.bin_id:
                response = await client.post(
                    f"{self.BASE_URL}/b",
                    data=data,
                    headers=self._get_headers(),
                )
                if response.status_code >= 400:
                    raise RuntimeError(f"Failed to create bin: {response.data}")
                if isinstance(response.data, dict):
                    self.bin_id = response.data.get("metadata", {}).get("id")
            else:
                response = await client.put(
                    f"{self.BASE_URL}/b/{self.bin_id}",
                    data=data,
                    headers=self._get_headers(),
                )
                if response.status_code >= 400:
                    raise RuntimeError(f"Failed to update bin: {response.data}")

    async def create(self, book: BookEntity) -> BookEntity:
        async with self._write_lock:
            data = await self._read_data()

            if any(book_dict["author"] == book.author and book_dict["name"] == book.name for book_dict in data):
                raise BookAlreadyExistsException(f"Book '{book.name}' by '{book.author}' already exists")

            book_dict = domain_to_json_dict(book)
            data.append(book_dict)
            await self._write_data(data)
        return book

    async def get(self, uuid: UUID) -> BookEntity | None:
        data = await self._read_data()
        uuid_str = str(uuid)

        for book_dict in data:
            if book_dict["uuid"] == uuid_str:
                return dict_to_domain(book_dict)

        return None

    async def exists(self, author: str, name: str) -> bool:
        data = await self._read_data()
        return any(book_dict["author"] == author and book_dict["name"] == name for book_dict in data)

    async def update(self, uuid: UUID, book: BookEntity) -> BookEntity:
        async with self._write_lock:
            data = await self._read_data()
            uuid_str = str(uuid)

            for book_dict in data:
                if (
                    book_dict["uuid"] != uuid_str
                    and book_dict["author"] == book.author
                    and book_dict["name"] == book.name
                ):
                    raise BookAlreadyExistsException(f"Book '{book.name}' by '{book.author}' already exists")

            for i, book_dict in enumerate(data):
                if book_dict["uuid"] == uuid_str:
                    updated_book = BookEntity(
                        uuid=book.uuid,
                        created_at=dict_to_domain(book_dict).created_at,
                        updated_at=datetime.now(UTC),
                        name=book.name,
                        author=book.author,
                        year=book.year,
                        pages=book.pages,
                        genre=book.genre,
                        availability=book.availability,
                        metadata=book.metadata,
                    )
                    data[i] = domain_to_json_dict(updated_book)
                    await self._write_data(data)
                    return updated_book

            return None

    async def delete(self, uuid: UUID) -> bool:
        async with self._write_lock:
            data = await self._read_data()
            uuid_str = str(uuid)
            initial_length = len(data)

            data = [book_dict for book_dict in data if book_dict["uuid"] != uuid_str]

            if len(data) < initial_length:
                await self._write_data(data)
                return True

            return False

    async def list(
        self,
        filters: BookFilters | None = None,
        pagination: PaginationSpec | None = None,
        sort: SortSpec | None = None,  # noqa: ARG002
    ) -> QueryResult[BookEntity]:
        data = await self._read_data()

        books = [dict_to_domain(book_dict) for book_dict in data]

        if filters:
            books = self._apply_filters(books, filters)

        total_count = len(books)

        if pagination:
            offset = pagination.offset or 0
            limit = pagination.limit or 0
            books = books[offset : offset + limit] if limit > 0 else books[offset:]
        else:
            offset = 0
            limit = 0

        return QueryResult[BookEntity](
            count=total_count,
            offset=offset,
            limit=limit,
            data=books,
        )

    def _apply_filters(self, books: list[BookEntity], filters: BookFilters) -> list[BookEntity]:
        result = books

        if filters.name:
            if filters.search_mode == "icontains":
                result = [b for b in result if filters.name.lower() in b.name.lower()]
            else:
                result = [b for b in result if b.name == filters.name]

        if filters.author:
            if filters.search_mode == "icontains":
                result = [b for b in result if filters.author.lower() in b.author.lower()]
            else:
                result = [b for b in result if b.author == filters.author]

        if filters.availability:
            result = [b for b in result if b.availability == filters.availability]

        return result
