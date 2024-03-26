from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, field_validator
from typing import Optional, List
from datetime import datetime

app = FastAPI()


class Book(BaseModel):
    id: Optional[int] = None
    title: str
    author: str
    description: str
    published_year: int

    @field_validator("published_year")
    def validate_published_year(cls, value):
        current_year = datetime.now().year
        if value > current_year:
            raise ValueError('published_year must not be in the future.')
        return value


fake_data = {
    "id": 1,
    "title": "노인",
    "author": "나",
    "description": "자고 싶어요..",
    "published_year": 2024,
}


books_db: List[Book] = []  # Fake DB


@app.on_event("startup")
async def startup_event():
    books_db.append(Book(**fake_data))


@app.post("/books/", response_model=Book)
def add_book(book: Book):
    book.id = len(books_db) + 1
    books_db.append(book)
    return book


@app.get("/books/", response_model=List[Book])
def read_books():
    return books_db


@app.get("/books/{book_id}/", response_model=Book)
def read_book(book_id: int):
    for book in books_db:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")


@app.put("/books/{book_id}/", response_model=Book)
def update_book(book_id: int, updated_book: Book):
    for index, book in enumerate(books_db):
        if book.id == book_id:
            updated_book.id = book_id
            books_db[index] = updated_book
            return updated_book
    raise HTTPException(status_code=404, detail="Book not found")


@app.delete("/books/{book_id}/")
def delete_book(book_id: int):
    for index, book in enumerate(books_db):
        if book.id == book_id:
            del books_db[index]
            return {"message": "Book deleted"}
    raise HTTPException(status_code=404, detail="Book not found")


# 심화 기능 - 도서 검색
@app.get("/books/search/", response_model=List[Book])
def search_book(title: Optional[str] = None, author: Optional[str] = None, published_year: Optional[int] = None):
    results = books_db
    if title:
        results = [book for book in results if title.lower() in book.title.lower()]
    if author:
        results = [book for book in results if author.lower() in book.author.lower()]
    if published_year:
        results = [book for book in results if book.published_year == published_year]
    return results


