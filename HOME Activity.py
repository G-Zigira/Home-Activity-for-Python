import json
import os
from datetime import datetime


class Book:

    def __init__(self, title, author, year, genre):

        self.id = self.next_id()

        self.title = title
        self.author = author
        self.year = year
        self.genre = genre
        self.isborrowed = False

        self.created_at = str(datetime.now())
        self.updated_at = str(datetime.now())

        self.filename = f"book{self.id}.json"

        self.save()

    @staticmethod
    def next_id():

        numbers = []

        for file in os.listdir():

            if file.startswith("book") and file.endswith(".json"):

                num = file.replace("book", "").replace(".json", "")
                numbers.append(int(num))

        return max(numbers, default=0) + 1

    
    def save(self):

        data = self.__dict__

        with open(self.filename, "w") as file:
            json.dump(data, file, indent=4)

    def borrow(self):

        if self.isborrowed:
            print("Book already borrowed")

        else:
            self.isborrowed = True
            self.updated_at = str(datetime.now())

            self.save()

            print(f"{self.title} borrowed")

    
    def display(self):

        print(f"""
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


book1 = Book("1984", "George Orwell", 1949, "Dystopian")

book2 = Book("MLBB", "Balmond Sunfire", 1789, "Fantasy")


book1.borrow()

book1.display()


loaded_book = Book.load("book1.json")

print("Loaded From JSON")

loaded_book.display()