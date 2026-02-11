import os


class Book:
    def __init__(self, title, author, status="доступна"):
        self.title = title
        self.author = author
        self.status = status

    def __str__(self):
        return f"{self.title} ({self.author}) — {self.status}"


class Person:
    def __init__(self, name):
        self._name = name

    def get_name(self):
        return self._name


class User(Person):
    def __init__(self, name, borrowed_books=None):
        super().__init__(name)
        self.borrowed_books = borrowed_books if borrowed_books else []

    def menu(self, library):
        while True:
            print("\n1. Просмотреть доступные книги")
            print("2. Взять книгу")
            print("3. Вернуть книгу")
            print("4. Мои книги")
            print("0. Назад")

            choice = input("Выбор: ").strip()

            if choice not in ("1", "2", "3", "4", "0"):
                print("Выберите корректный пункт")
                continue

            if choice == "1":
                library.show_available_books()
            elif choice == "2":
                library.borrow_book(self)
            elif choice == "3":
                library.return_book(self)
            elif choice == "4":
                if self.borrowed_books:
                    print("Ваши книги:", self.borrowed_books)
                else:
                    print("Вы не взяли ни одной книжки(неуч)")
            elif choice == "0":
                print("Спуматюма пуматюма поу пума пума тей")
                break


class Librarian(Person):
    def menu(self, library):
        while True:
            print("\n1. Добавить книгу")
            print("2. Удалить книгу")
            print("3. Зарегистрировать пользователя")
            print("4. Просмотреть пользователей")
            print("5. Просмотреть все книги")
            print("0. Назад")

            choice = input("Выбор: ").strip()

            if choice not in ("1", "2", "3", "4", "5", "0"):
                print("Выберите кореектное число")
                continue

            if choice == "1":
                library.add_book()
            elif choice == "2":
                library.remove_book()
            elif choice == "3":
                library.register_user()
            elif choice == "4":
                library.show_users()
            elif choice == "5":
                library.show_all_books()
            elif choice == "0":
                print("бабушка рассказала мне этот рецепт и после этого муж...\033[3;34mчитать дальше\033[0m")
                break


class Library:
    def __init__(self):
        self.books = []
        self.users = {}
        self.load_data()

    def load_data(self):
        try:
            if os.path.exists("books.txt"):
                with open("books.txt", "r", encoding="utf-8") as f:
                    for line in f:
                        parts = line.strip().split(";")
                        if len(parts) == 3:
                            title, author, status = parts
                            self.books.append(Book(title, author, status))

            if os.path.exists("users.txt"):
                with open("users.txt", "r", encoding="utf-8") as f:
                    for line in f:
                        parts = line.strip().split(";")
                        if len(parts) == 2:
                            name, books = parts
                            self.users[name] = User(
                                name, books.split(",") if books else []
                            )
        except Exception as e:
            print("Ошибка при загрузке данных:", e)

    def save_data(self):
        try:
            with open("books.txt", "w", encoding="utf-8") as f:
                for book in self.books:
                    f.write(f"{book.title};{book.author};{book.status}\n")

            with open("users.txt", "w", encoding="utf-8") as f:
                for user in self.users.values():
                    books = ",".join(user.borrowed_books)
                    f.write(f"{user.get_name()};{books}\n")
        except Exception as e:
            print("Ошибка при сохранении данных:", e)

    def add_book(self):
        title = input("Название: ").strip()
        author = input("Автор: ").strip()

        if not title or not author:
            print("Название и автор не должны быть пустыми.")
            return

        self.books.append(Book(title, author))
        print("Книга добавлена")

    def remove_book(self):
        title = input("Название книги: ").strip()
        for book in self.books:
            if book.title == title:
                self.books.remove(book)
                print("Книга удалена")
                return
        print("Книга не найдена")

    def register_user(self):
        name = input("Имя пользователя: ").strip()

        if not name:
            print("Имя не должно быть пустым")
            return

        if name not in self.users:
            self.users[name] = User(name)
            print("Пользователь зарегистрирован")
        else:
            print("такой пользователь уже существует")

    def show_users(self):
        if not self.users:
            print("Нет зарегистрированных пользователей.")
            return
        for name in self.users:
            print(name)

    def show_all_books(self):
        if not self.books:
            print("В библиотеке нет книг.")
            return
        for book in self.books:
            print(book)

    def show_available_books(self):
        available = [book for book in self.books if book.status == "доступна"]
        if not available:
            print("Нет доступных книг.")
            return
        for book in available:
            print(book)

    def borrow_book(self, user):
        title = input("Название книги: ").strip()
        for book in self.books:
            if book.title == title:
                if book.status == "доступна":
                    book.status = "выдана"
                    user.borrowed_books.append(title)
                    print("Книга выдана")
                else:
                    print("Книга не доступна")
                return
        print("Книга не найдена")

    def return_book(self, user):
        title = input("Название книги: ").strip()

        if title not in user.borrowed_books:
            print("Вы не брали такую книгу")
            return

        user.borrowed_books.remove(title)
        for book in self.books:
            if book.title == title:
                book.status = "доступна"
        print("Книга возвращена")


def main():
    library = Library()

    while True:
        print("\nВыберите роль:")
        print("1. Библиотекарь")
        print("2. Пользователь")
        print("0. Выход")

        choice = input("Выбор: ").strip()

        if choice not in ("1", "2", "0"):
            print("Выбран некорректный пункт")
            continue

        if choice == "1":
            name = input("Имя библиотекаря: ").strip()
            Librarian(name).menu(library)
        elif choice == "2":
            name = input("Имя пользователя: ").strip()
            if name in library.users:
                library.users[name].menu(library)
            else:
                print("Пользователь не найден")
        elif choice == "0":
            library.save_data()
            print("Данные сохранены. мммармок пам пам     пам     пам пам.")
            break


if __name__ == "__main__":
    main()
