from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional


app = FastAPI()


class Book(BaseModel):
    id: Optional[int] = None
    title: str
    author: str
    description: str
    published_year: int


books_db = []  # Fake DB


@app.post("/books/")
def add_book(book: Book):
    book.id = len(books_db) + 1
    books_db.append(book.dict())
    return book


@app.get("/books/")
def read_books():
    return books_db


@app.get("/books/{book_id}/")
def read_book(book_id: int):
    for book in books_db:
        if book["id"] == book_id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")


@app.put("/books/{book_id}/")
def update_book(book_id: int, updated_book: Book):
    for index, book in enumerate(books_db):
        if book["id"] == book_id:
            updated_book_dict = updated_book.dict()
            updated_book_dict["id"] = book_id
            books_db[index] = updated_book_dict
            return updated_book_dict
    raise HTTPException(status_code=404, detail="Book not found")


@app.delete("/books/{book_id}/")
def delete_book(book_id: int):
    for index, book in enumerate(books_db):
        if book["id"] == book_id:
            del books_db[index]
            return {"message": "Book deleted"}
    raise HTTPException(status_code=404, detail="Book not found")


