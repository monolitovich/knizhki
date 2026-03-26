import os
import pickle


class Book:
    def __init__(self, title, author):
        self.title = title
        self.author = author
        self.is_borrowed = False

    def __str__(self):
        status = "Занята" if self.is_borrowed else "Доступна"
        return f"{self.title} — {self.author} ({status})"


class User:
    def __init__(self, name):
        self.name = name
        self.borrowed_books = []

    def __str__(self):
        books = ', '.join(self.borrowed_books) if self.borrowed_books else 'нет'
        return f"{self.name}, книги: {books}"


class Library:
    def __init__(self):
        self.books = []
        self.users = {}
        self.load_data()

    def add_book(self, title, author):
        self.books.append(Book(title, author))
        print("Книга добавлена!")

    def register_user(self, name):
        if name not in self.users:
            self.users[name] = User(name)
            print("Пользователь зарегистрирован!")
        else:
            print("Пользователь уже существует")

    def borrow_book(self, user_name, book_title):
        if user_name not in self.users:
            print("Пользователь не найден")
            return

        for book in self.books:
            if book.title == book_title and not book.is_borrowed:
                book.is_borrowed = True
                self.users[user_name].borrowed_books.append(book_title)
                print("Книга выдана!")
                return

        print("Книга недоступна")

    def return_book(self, user_name, book_title):
        if user_name not in self.users:
            print("Пользователь не найден")
            return

        for book in self.books:
            if book.title == book_title and book.is_borrowed:
                book.is_borrowed = False
                if book_title in self.users[user_name].borrowed_books:
                    self.users[user_name].borrowed_books.remove(book_title)
                print("Книга возвращена!")
                return

        print("Ошибка возврата")

    def show_books(self):
        if not self.books:
            print("Нет книг")
            return
        for book in self.books:
            print(book)

    def show_users(self):
        if not self.users:
            print("Нет пользователей")
            return
        for user in self.users.values():
            print(user)

    def save_data(self):
        try:
            data = {
                "books": self.books,
                "users": self.users
            }
            with open("library.pkl", "wb") as f:
                pickle.dump(data, f)
            print("Данные сохранены в pickle файл")
        except Exception as e:
            print("Ошибка при сохранении:", e)

    def load_data(self):
        try:
            if os.path.exists("library.pkl"):
                with open("library.pkl", "rb") as f:
                    data = pickle.load(f)
                    self.books = data.get("books", [])
                    self.users = data.get("users", {})
                print("Данные успешно загружены из pickle файла")
            else:
                self.books = []
                self.users = {}
        except Exception as e:
            print("Ошибка при загрузке:", e)
            self.books = []
            self.users = {}

    def show_pickle_binary_info(self):
        try:
            if os.path.exists("library.pkl"):
                with open("library.pkl", "rb") as f:
                    binary_data = f.read()

                print("\nСодержимое файла:")
                print("Бинарные данные:", binary_data)
                print("\nШестнадцатеричный вид:", binary_data.hex())

            else:
                print("Файл library.pkl не найден")
        except Exception as e:
            print("Ошибка при анализе pickle файла:", e)


def main():
    library = Library()

    while True:
        print("\n1. Добавить книгу")
        print("2. Зарегистрировать пользователя")
        print("3. Выдать книгу")
        print("4. Вернуть книгу")
        print("5. Показать книги")
        print("6. Показать пользователей")
        print("7. Прочитать файл")
        print("0. Выход")

        choice = input("Выберите действие: ")

        if choice == "1":
            title = input("Название: ")
            author = input("Автор: ")
            library.add_book(title, author)

        elif choice == "2":
            name = input("Имя пользователя: ")
            library.register_user(name)

        elif choice == "3":
            name = input("Имя пользователя: ")
            title = input("Название книги: ")
            library.borrow_book(name, title)

        elif choice == "4":
            name = input("Имя пользователя: ")
            title = input("Название книги: ")
            library.return_book(name, title)

        elif choice == "5":
            library.show_books()

        elif choice == "6":
            library.show_users()

        elif choice == "7":
            library.show_pickle_binary_info()

        elif choice == "0":
            library.save_data()
            print("Выход")
            break

        else:
            print("Неверный ввод")


if __name__ == "__main__":
    main()