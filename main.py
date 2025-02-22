from fastapi import FastAPI, HTTPException, status
from database import session_dependency, create_db_and_tables
from models import Book, BookCreateModel, BookReadModel, BookUpdateModel
from sqlmodel import Session, select


app = FastAPI()


@app.on_event("startup")
async def startup():
    create_db_and_tables()


@app.post("/books/", response_model=BookReadModel)
def create_a_book(book: BookCreateModel, session: session_dependency):
    book = Book.model_validate(book)
    session.add(book)
    session.commit()
    session.refresh(book)
    return book


@app.get("/books/{book_id}", response_model=BookReadModel)
def read_a_book(book_id: int, session: session_dependency):
    book = session.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail=f"Book with id {book_id} not found")
    return book


# get all books
@app.get("/books/", response_model=list[BookReadModel])
def read_all_books(session: session_dependency):
    query = select(Book)
    books = session.exec(query)
    return books


# https://sqlmodel.tiangolo.com/tutorial/fastapi/update/#create-the-update-path-operation
@app.patch("/books/{book_id}", response_model=BookReadModel)
def update_a_book(book_id: int, book: BookUpdateModel, session: session_dependency):
    db_book = session.get(Book, book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail=f"Book with id {book_id} not found")

    book_data = book.model_dump(exclude_unset=True) # exclude fields that are not set
    db_book.sqlmodel_update(book_data)              # update the fields that are set

    session.add(db_book)
    session.commit()
    session.refresh(db_book)
    return db_book


@app.delete("/books/{book_id}", response_model=dict)
def delete_a_book(book_id: int, session: session_dependency):
    book = session.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail=f"Book with id {book_id} not found")
    session.delete(book)
    session.commit()
    return {"message": f"Book with {book_id} deleted successfully"}
