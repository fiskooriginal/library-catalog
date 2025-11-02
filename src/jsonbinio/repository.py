from datetime import datetime
from uuid import UUID, uuid4

import aiohttp

from src.library_catalog.schemas import Book, BookCreate, BookUpdate


class JSONBinRepository:
    BASE_URL = "https://api.jsonbin.io/v3"

    def __init__(self, api_key: str, bin_id: str | None = None):
        self.api_key = api_key
        self.bin_id = bin_id
        self._headers = {
            "X-Master-Key": self.api_key,
            "Content-Type": "application/json",
        }

    async def _read_data(self) -> list[dict]:
        if not self.bin_id:
            return []

        async with (
            aiohttp.ClientSession() as session,
            session.get(
                f"{self.BASE_URL}/b/{self.bin_id}/latest",
                headers=self._headers,
            ) as response,
        ):
            response.raise_for_status()
            data = await response.json()
            return data.get("record", [])

    async def _write_data(self, data: list[dict]):
        if not self.bin_id:
            async with (
                aiohttp.ClientSession() as session,
                session.post(
                    f"{self.BASE_URL}/b",
                    json=data,
                    headers=self._headers,
                ) as response,
            ):
                response.raise_for_status()
                result = await response.json()
                self.bin_id = result["metadata"]["id"]
        else:
            async with (
                aiohttp.ClientSession() as session,
                session.put(
                    f"{self.BASE_URL}/b/{self.bin_id}",
                    json=data,
                    headers=self._headers,
                ) as response,
            ):
                response.raise_for_status()

    async def create(self, book_data: BookCreate) -> Book:
        data = await self._read_data()
        now = datetime.now()

        book_dict = {
            "uuid": str(uuid4()),
            "created_at": now.isoformat(),
            "updated_at": now.isoformat(),
            **book_data.model_dump(),
        }

        data.append(book_dict)
        await self._write_data(data)

        return Book(**book_dict)

    async def get_by_id(self, uuid: UUID) -> Book | None:
        data = await self._read_data()
        uuid_str = str(uuid)

        for book_dict in data:
            if book_dict["uuid"] == uuid_str:
                return Book(**book_dict)

        return None

    async def get_all(self) -> list[Book]:
        data = await self._read_data()
        return [Book(**book_dict) for book_dict in data]

    async def update(self, uuid: UUID, book_data: BookUpdate) -> Book | None:
        data = await self._read_data()
        uuid_str = str(uuid)

        for i, book_dict in enumerate(data):
            if book_dict["uuid"] == uuid_str:
                book_dict.update(book_data.model_dump())
                book_dict["updated_at"] = datetime.now().isoformat()
                data[i] = book_dict
                await self._write_data(data)
                return Book(**book_dict)

        return None

    async def delete(self, uuid: UUID) -> bool:
        data = await self._read_data()
        uuid_str = str(uuid)
        initial_length = len(data)

        data = [book_dict for book_dict in data if book_dict["uuid"] != uuid_str]

        if len(data) < initial_length:
            await self._write_data(data)
            return True

        return False

    def get_bin_id(self) -> str | None:
        return self.bin_id
