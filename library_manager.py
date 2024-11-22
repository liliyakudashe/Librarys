import json
from typing import List, Dict, Union


DATA_FILE = "library.json"


def load_data() -> List[Dict]:
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_data(data: List[Dict]) -> None:
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def add_book(title: str, author: str, year: int) -> None:
    books = load_data()
    book_id = max((book["id"] for book in books), default=0) + 1
    books.append({"id": book_id, "title": title, "author": author, "year": year, "status": "в наличии"})
    save_data(books)
    print(f"Книга '{title}' успешно добавлена с id {book_id}.")


def delete_book(book_id: int) -> None:
    books = load_data()
    updated_books = [book for book in books if book["id"] != book_id]
    if len(books) == len(updated_books):
        print(f"Книга с id {book_id} не найдена.")
    else:
        save_data(updated_books)
        print(f"Книга с id {book_id} успешно удалена.")


def search_books(key: str, value: Union[str, int]) -> List[Dict]:
    books = load_data()
    result = [book for book in books if str(book[key]).lower() == str(value).lower()]
    return result


def display_books() -> None:
    books = load_data()
    if not books:
        print("Библиотека пуста.")
    else:
        for book in books:
            print(f"ID: {book['id']}, Название: {book['title']}, Автор: {book['author']}, "
                  f"Год: {book['year']}, Статус: {book['status']}")


def update_status(book_id: int, new_status: str) -> None:
    if new_status not in ["в наличии", "выдана"]:
        print("Некорректный статус. Возможные значения: 'в наличии', 'выдана'.")
        return
    books = load_data()
    for book in books:
        if book["id"] == book_id:
            book["status"] = new_status
            save_data(books)
            print(f"Статус книги с id {book_id} успешно обновлен на '{new_status}'.")
            return
    print(f"Книга с id {book_id} не найдена.")


def main_menu() -> None:
    while True:
        print("\nМеню:")
        print("1. Добавить книгу")
        print("2. Удалить книгу")
        print("3. Найти книгу")
        print("4. Показать все книги")
        print("5. Изменить статус книги")
        print("6. Выйти")

        choice = input("Выберите действие: ").strip()

        if choice == "1":
            title = input("Введите название книги: ").strip()
            author = input("Введите автора книги: ").strip()
            year = input("Введите год издания книги: ").strip()
            if not year.isdigit():
                print("Год должен быть числом.")
                continue
            add_book(title, author, int(year))

        elif choice == "2":
            book_id = input("Введите ID книги, которую нужно удалить: ").strip()
            if not book_id.isdigit():
                print("ID должен быть числом.")
                continue
            delete_book(int(book_id))

        elif choice == "3":
            key = input("Введите критерий поиска (title, author, year): ").strip().lower()
            if key not in ["title", "author", "year"]:
                print("Некорректный критерий. Возможные значения: title, author, year.")
                continue
            value = input("Введите значение для поиска: ").strip()
            if key == "year" and not value.isdigit():
                print("Год должен быть числом.")
                continue
            results = search_books(key, value if key != "year" else int(value))
            if results:
                for book in results:
                    print(f"ID: {book['id']}, Название: {book['title']}, Автор: {book['author']}, "
                          f"Год: {book['year']}, Статус: {book['status']}")
            else:
                print("Книги по указанному критерию не найдены.")

        elif choice == "4":
            display_books()

        elif choice == "5":
            book_id = input("Введите ID книги: ").strip()
            if not book_id.isdigit():
                print("ID должен быть числом.")
                continue
            new_status = input("Введите новый статус (в наличии, выдана): ").strip()
            update_status(int(book_id), new_status)

        elif choice == "6":
            print("Выход из программы. До свидания!")
            break

        else:
            print("Некорректный выбор. Попробуйте снова.")

if __name__ == "__main__":
    main_menu()
