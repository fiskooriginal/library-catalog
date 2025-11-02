import asyncio
from pathlib import Path

from src.json.repository import JSONBookRepository
from src.library_catalog.enums import AvailabilityEnum
from src.library_catalog.schemas import BookCreate, BookUpdate


async def main():
    current_dir = Path(__file__).parent
    json_file = current_dir / "books.json"

    repo = JSONBookRepository(json_file)

    print("=== Создание книг ===")
    book1 = await repo.create(
        BookCreate(
            name="1984",
            author="George Orwell",
            year=1949,
            genre="Dystopian",
            pages=328,
            availability=AvailabilityEnum.IN_STOCK,
        )
    )
    print(f"Создана книга: {book1.name} by {book1.author} (UUID: {book1.uuid})")

    book2 = await repo.create(
        BookCreate(
            name="Brave New World",
            author="Aldous Huxley",
            year=1932,
            genre="Dystopian",
            pages=268,
            availability=AvailabilityEnum.IN_STOCK,
        )
    )
    print(f"Создана книга: {book2.name} by {book2.author} (UUID: {book2.uuid})")

    book3 = await repo.create(
        BookCreate(
            name="Fahrenheit 451",
            author="Ray Bradbury",
            year=1953,
            genre="Dystopian",
            pages=249,
            availability=AvailabilityEnum.IN_STOCK,
        )
    )
    print(f"Создана книга: {book3.name} by {book3.author} (UUID: {book3.uuid})")

    print("\n=== Получение всех книг ===")
    all_books = await repo.get_all()
    print(f"Всего книг в каталоге: {len(all_books)}")
    for book in all_books:
        print(f"  - {book.name} ({book.year}), {book.pages} стр., статус: {book.availability}")

    print("\n=== Поиск книги по ID ===")
    found_book = await repo.get_by_id(book2.uuid)
    if found_book:
        print(f"Найдена книга: {found_book.name} by {found_book.author}")
        print(f"  Год: {found_book.year}, Жанр: {found_book.genre}")
        print(f"  Страниц: {found_book.pages}, Статус: {found_book.availability}")

    print("\n=== Обновление книги ===")
    updated_book = await repo.update(
        book2.uuid,
        BookUpdate(
            name="Brave New World",
            author="Aldous Huxley",
            year=1932,
            genre="Dystopian",
            pages=268,
            availability=AvailabilityEnum.BORROWED,
        ),
    )
    if updated_book:
        print(f"Книга '{updated_book.name}' обновлена")
        print(f"  Новый статус: {updated_book.availability}")
        print(f"  Обновлено: {updated_book.updated_at}")

    print("\n=== Удаление книги ===")
    deleted = await repo.delete(book3.uuid)
    if deleted:
        print(f"Книга '{book3.name}' успешно удалена")

    print("\n=== Финальный список книг ===")
    final_books = await repo.get_all()
    print(f"Осталось книг: {len(final_books)}")
    for book in final_books:
        print(f"  - {book.name} by {book.author} [{book.availability}]")


if __name__ == "__main__":
    asyncio.run(main())
