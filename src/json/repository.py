import json
from datetime import datetime
from pathlib import Path
from uuid import UUID, uuid4

import aiofiles

from src.library_catalog.schemas import Book, BookCreate, BookUpdate


class JSONBookRepository:
    def __init__(self, file_path: str | Path):
        self.file_path = Path(file_path)
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        if not self.file_path.exists():
            self.file_path.parent.mkdir(parents=True, exist_ok=True)
            self.file_path.write_text("[]")

    async def _read_data(self) -> list[dict]:
        async with aiofiles.open(self.file_path) as f:
            content = await f.read()
            return json.loads(content)

    async def _write_data(self, data: list[dict]):
        async with aiofiles.open(self.file_path, "w") as f:
            content = json.dumps(data, indent=2, default=str)
            await f.write(content)

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
