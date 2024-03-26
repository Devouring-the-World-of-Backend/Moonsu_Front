from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()


class Book(BaseModel):
    id: int
    title: str
    author: str
    description: str
    published_year: int


books = []


@app.get("/book")
async def read_book():
    return books
