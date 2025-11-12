from uuid import UUID

from sqlalchemy import Select, delete, func, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.library_catalog.domain.entities.books import BookEntity
from src.library_catalog.domain.exceptions.books import BookAlreadyExistsException
from src.library_catalog.domain.repositories.books import BookRepositoryProtocol
from src.library_catalog.domain.vo.books import BookFilters, PaginationSpec, QueryResult, SortSpec
from src.library_catalog.infrastructure.persistence.mappers.books import (
    domain_to_dict,
    domain_to_model,
    model_to_domain,
)
from src.library_catalog.infrastructure.persistence.models.base import BaseModel
from src.library_catalog.infrastructure.persistence.models.books import BookModel


class BooksRepositorySqlAlchemyImpl(BookRepositoryProtocol):
    model: type[BaseModel] = BookModel

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, book: BookEntity) -> BookEntity:
        db_row = domain_to_model(book)
        self._session.add(db_row)
        try:
            await self._session.flush()
            await self._session.refresh(db_row)
        except IntegrityError as exc:
            raise BookAlreadyExistsException(f"Book '{book.name}' by '{book.author}' already exists") from exc
        return model_to_domain(db_row)

    async def get(self, uuid: UUID) -> BookEntity | None:
        statement: Select = select(self.model).where(self.model.uuid == uuid)
        result = await self._session.execute(statement)
        db_row: BaseModel | None = result.scalar_one_or_none()
        if db_row is None:
            return None
        return model_to_domain(db_row)

    async def exists(self, author: str, name: str) -> bool:
        statement = select(func.count(self.model.uuid)).where((self.model.author == author) & (self.model.name == name))
        result = await self._session.execute(statement)
        count = int(result.scalar() or 0)
        return count > 0

    async def update(self, uuid: UUID, book: BookEntity) -> BookEntity | None:
        db_row = select(self.model).where(self.model.uuid == uuid)
        result = await self._session.execute(db_row)
        db_row = result.scalar_one_or_none()
        if db_row is None:
            return None

        update_dict = domain_to_dict(book, exclude_none=True)
        try:
            await self._session.execute(update(self.model).where(self.model.uuid == uuid).values(**update_dict))
            await self._session.flush()
            await self._session.refresh(db_row)
        except IntegrityError as exc:
            raise BookAlreadyExistsException(f"Book '{book.name}' by '{book.author}' already exists") from exc
        return model_to_domain(db_row)

    async def delete(self, uuid: UUID) -> bool:
        statement = delete(self.model).where(self.model.uuid == uuid)
        result = await self._session.execute(statement)
        return result.rowcount > 0

    async def list(
        self,
        filters: BookFilters | None = None,
        pagination: PaginationSpec | None = None,
        sort: SortSpec | None = None,
    ) -> QueryResult[BookEntity]:
        base = select(self.model)
        base = self._apply_filters(base, filters)
        base = self._apply_sort(base, sort)

        count_statement = select(func.count()).select_from(base.order_by(None).subquery())
        total_result = await self._session.execute(count_statement)
        total_count = int(total_result.scalar() or 0)

        if pagination and pagination.limit is not None:
            base = base.limit(pagination.limit)
        if pagination and pagination.offset is not None:
            base = base.offset(pagination.offset)

        rows = await self._session.execute(base)
        rows = rows.scalars().all()
        data = [model_to_domain(row) for row in rows]

        return QueryResult[BookEntity](
            count=total_count,
            offset=(pagination.offset if pagination else 0),
            limit=(pagination.limit if pagination else 0),
            data=data,
        )

    def _apply_filters(self, stmt: Select, filters: BookFilters | None) -> Select:
        if not filters:
            return stmt
        if filters.name:
            stmt = stmt.where(
                self.model.name.ilike(f"%{filters.name}%")
                if filters.search_mode == "icontains"
                else self.model.name == filters.name
            )
        if filters.author:
            stmt = stmt.where(
                self.model.author.ilike(f"%{filters.author}%")
                if filters.search_mode == "icontains"
                else self.model.author == filters.author
            )
        if filters.genre:
            stmt = stmt.where(
                self.model.genre.ilike(f"%{filters.genre}%")
                if filters.search_mode == "icontains"
                else self.model.genre == filters.genre
            )
        if filters.availability:
            stmt = stmt.where(self.model.availability == str(filters.availability))
        if filters.year is not None:
            stmt = stmt.where(self.model.year == filters.year)
        if filters.year_from is not None:
            stmt = stmt.where(self.model.year >= filters.year_from)
        if filters.year_to is not None:
            stmt = stmt.where(self.model.year <= filters.year_to)
        if filters.pages_min is not None:
            stmt = stmt.where(self.model.pages >= filters.pages_min)
        if filters.pages_max is not None:
            stmt = stmt.where(self.model.pages <= filters.pages_max)
        if filters.with_metadata:
            stmt = stmt.where(
                (self.model.cover_image_url.is_not(None))
                | (self.model.description.is_not(None))
                | (self.model.rating.is_not(None))
            )
        return stmt

    def _apply_sort(self, stmt: Select, sort: SortSpec | None) -> Select:
        if not sort:
            return stmt.order_by(self.model.created_at.desc())
        field_map = {
            "name": self.model.name,
            "author": self.model.author,
            "genre": self.model.genre,
            "year": self.model.year,
            "pages": self.model.pages,
            "availability": self.model.availability,
            "rating": self.model.rating,
            "created_at": self.model.created_at,
            "updated_at": self.model.updated_at,
        }
        column = field_map.get(sort.field)
        if not column:
            return stmt.order_by(self.model.created_at.desc())
        return stmt.order_by(column.desc() if sort.direction == "desc" else column.asc())
