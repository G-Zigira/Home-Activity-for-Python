import json
import os
from datetime import datetime


class BaseModel:
    def __init__(self):
        self.id = self.next_id()
        self.created_at = str(datetime.now())
        self.updated_at = str(datetime.now())

    @classmethod
    def next_id(cls):
        numbers = []

        prefix = cls.__name__.lower()

        for file in os.listdir():
            if file.startswith(prefix) and file.endswith(".json"):
                num = file.replace(prefix, "").replace(".json", "")
                if num.isdigit():
                    numbers.append(int(num))

        return max(numbers, default=0) + 1

    def save(self):
        self.updated_at = str(datetime.now())

        data = self.__dict__

        with open(self.filename, "w") as file:
            json.dump(data, file, indent=4)


class Book(BaseModel):
    def __init__(self, title, author, year, genre):
        super().__init__()

        self.title = title
        self.author = author
        self.year = year
        self.genre = genre
        self.isborrowed = False

        self.filename = f"book{self.id}.json"

        self.save()

    def borrow(self):
        if self.isborrowed:
            print("Book already borrowed")
        else:
            self.isborrowed = True
            self.save()
            print(f"{self.title} borrowed")

    def display(self):
        print(f"""
BOOK DETAILS
ID: {self.id}
Title: {self.title}
Author: {self.author}
Year: {self.year}
Genre: {self.genre}
Borrowed: {self.isborrowed}
Created: {self.created_at}
Updated: {self.updated_at}
""")

    @classmethod
    def load(cls, filename):
        with open(filename, "r") as file:
            data = json.load(file)

        book = cls.__new__(cls)
        book.__dict__ = data
        return book


class User(BaseModel):
    def __init__(self, name, email):
        super().__init__()

        self.name = name
        self.email = email
        self.borrowed_books = []

        self.filename = f"user{self.id}.json"

        self.save()

    def borrow_book(self, book):
        if book.isborrowed:
            print("Cannot borrow, book already taken")
        else:
            book.borrow()
            self.borrowed_books.append(book.title)
            self.save()

    def display(self):
        print(f"""
USER DETAILS
ID: {self.id}
Name: {self.name}
Email: {self.email}
Borrowed Books: {self.borrowed_books}
Created: {self.created_at}
Updated: {self.updated_at}
""")


book1 = Book("1984", "George Orwell", 1949, "Dystopian")
book2 = Book("MLBB", "Balmond Sunfire", 1789, "Fantasy")

user1 = User("Lucas", "lucas@email.com")

user1.borrow_book(book1)

book1.display()
user1.display()


loaded_book = Book.load("book1.json")

print("Loaded From JSON")
loaded_book.display()