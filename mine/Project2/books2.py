from typing import Optional

from fastapi import FastAPI, Body, Path, Query
from pydantic import BaseModel, Field

app = FastAPI()


class BookRequest(BaseModel):
    id: Optional[int] = Field(title='id is not needed')
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=0, lt=6)
    published_date: int = Field(gt=1999, lt=2031)

    class Config:
        schema_extra = {
            'example': {
                'title': 'A new book',
                'author': 'codingwithroby',
                'description': 'A new description of a book',
                'rating': 5,
                'published_date': 2029
            }
        }


class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int
    published_date: int

    def __init__(self, id, title, author, description, rating, published_date):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date

    def __str__(self):
        return f"Book: id={self.id}, title={self.title}, author={self.author}, description={self.description}, " \
               f"rating={self.rating} "


BOOKS = [
    Book(1, 'Computer Science Pro', 'codingwithroby', 'A very nice book!', 5, 2030),
    Book(2, 'Be Fast with Fast API', 'codingwithroby', 'A great book!', 5, 2029),
    Book(3, 'Master Endpoints', 'codingwithroby', 'An awesome book!', 5, 2023),
    Book(4, 'HP1', 'Author 1', 'Book Description', 2, 2022),
    Book(5, 'HP2', 'Author 2', 'Book Description', 3, 2021),
    Book(6, 'HP3', 'Author 3', 'Book Description', 1, 2020),
]


@app.get("/books")
async def read_all_books():
    return BOOKS


@app.get("/books/{book_id}")
async def read_book(book_id: int = Path(gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            return book


@app.get("/books/publish/")
async def read_book_by_published_date(published_date: int = Query(gt=1999, lt=2031)):
    print('in read_book_by_published_date')
    books_to_return = []
    for book in BOOKS:
        if book.published_date == published_date:
            books_to_return.append(book)
    return books_to_return


@app.get("/books/")
async def read_book_by_rating(rating: int = Query(gt=0, lt=6)):
    books_to_return = []
    for book in BOOKS:
        if book.rating == rating:
            books_to_return.append(book)
    return books_to_return


@app.post("/create-book")
async def create_book(book_request: BookRequest):
    book = Book(**book_request.dict())
    BOOKS.append(find_book_id(book))


def find_book_id(book: Book):
    if len(BOOKS) > 0:
        book.id = BOOKS[-1].id + 1
    else:
        book.id = 1
    return book


@app.put("/books/update_book")
async def update_book(book: BookRequest):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = Book(**book.dict())


@app.delete("/books/{book_id}")
async def delete_book(book_id: int = Path(gt=0)):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            break
