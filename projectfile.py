import re

def isFileExist(func):
    def wrapper(self, *args, **kwargs):
        try:
            with open(self.filename, 'r'):
                pass
        except FileNotFoundError:
            print(f"Error: Файл {self.filename} не найдено.")
            return
        return func(self, *args, **kwargs)
    return wrapper

class Book:
    def __init__(self, title, author, year, genre, score):
        self.title = title
        self.author = author
        self.year = year
        self.genre = genre
        self.score = score

    def __str__(self):
        return f"Title: {self.title}, Author: {self.author}, Year: {self.year}, Genre: {self.genre}, Score: {self.score}"

    def __eq__(self, other):
        return self.title == other.title and self.author == other.author

    def __lt__(self, other):
        return self.score < other.score

    def __gt__(self, other):
        return self.score > other.score

class EBook(Book):
    def __init__(self, title, author, year, genre, score, fileformat, filesize):
        super().__init__(title, author, year, genre, score)
        self.fileformat = fileformat
        self.filesize = filesize

    def __str__(self):
        return f"Title: {self.title}, Author: {self.author}, Year: {self.year}, Genre: {self.genre}, Score: {self.score}, Format: {self.fileformat}, Size: {self.filesize} MB"
    
class Library:
    def __init__(self,filename="library.txt"):
        self.book = []
        self.filename = filename
        self.loadfromfile()

    def addBook(self, book):
        if book not in self.book:
            self.book.append(book)
            print(f"Книга {book.title} успешно добавлена!")
            self.savetofile()
        else:
            print(f"Книга {book.title} уже существует.")

    @isFileExist
    def loadfromfile(self):
        try:
            with open(self.filename, 'r') as file:
                for line in file.readlines():
                    linepart = line.strip().split(',')
                    title, author, year, genre, score = linepart[:5]
                    if len(linepart) == 7:
                        fileformat = linepart[5]
                        filesize = float(linepart[6])
                        book = EBook(title, author, int(year), genre, int(score), fileformat, filesize)
                    else:
                        book = Book(title,author,int(year),genre,int(score))
                    self.book.append(book)
        except FileNotFoundError:
            print("Error: Файл не найдено")
    
    def savetofile(self):
        with open(self.filename, 'w') as file:
            for book in self.book:
                if isinstance(book,EBook):
                    file.write(f"{book.title},{book.author},{book.year},{book.genre},{book.score},{book.fileformat},{book.filesize}\n")
                else:
                    file.write(f"{book.title},{book.author},{book.year},{book.genre},{book.score}\n")
    
    def searchbyregax(self, pattern):
        regex = re.compile(pattern, re.IGNORECASE)
        result = [book for book in self.book if regex.search(book.title) or regex.search(book.author)]
        return result

def main():
    library = Library()

    while True:
        command = input("Введите команду(search, addbook, help, exit): ").strip().lower()

        if command == "addbook":
            title = input("Введите название книги: ").strip()
            author = input("Введите имя автора: ").strip()
            year = int(input("Введите год выпуска: ").strip())
            genre = input("Введите жанр: ").strip()
            score = int(input("Введите популярность score(0-100): ").strip())

            booktype = input("Это електроная книга? (yes/no): ").strip().lower()

            if booktype == "yes":
                fileformat = input("Введите формат файла(pdf, epub): ").strip()
                filesize = float(input("Введите розмер файла в MB: ").strip())
                book = EBook(title, author, year, genre, score, fileformat, filesize)
            else:
                book = Book(title,author,year,genre,score)

            if 0 <= score <= 100:
                library.addBook(book)
            else:
                print("Неправилно введеные score. Пожалуйста введите от 0 до 100.")
            
        elif command == "search":
            pattern = input("Введите параметры для поиска (title or author): ").strip()
            foundbook = library.searchbyregax(pattern)
            if foundbook:
                for book in foundbook:
                    print(book)
            else:
                print("Книгу не найдно")

        elif command == "help":
            print("Все команды: ")
            print("addbook - добовляет новую книгу в библиотеку.")
            print("search - поиск книги по названию(title) или автору(author).")
            print("help - показует сообщение со всеми командами.")
            print("exit - выход из программы.")

        elif command == "exit":
            print("Выход из программы.")
            break

        else:
            print("Неправильная коммадна. Введите 'Help' для просмотра всех комманд")

if __name__ == "__main__":
    main()