from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
import os
from . import models, schemas, crud, database

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/books/", response_model=list[schemas.BookResponse])
def read_books(db: Session = Depends(database.get_db)):
    return crud.get_books(db)

@app.post("/books/", response_model=schemas.BookResponse)
def add_book(book: schemas.BookCreate, db: Session = Depends(database.get_db)):
    return crud.create_book(db, book)

@app.put("/books/{book_id}", response_model=schemas.BookResponse)
def update_book(book_id: int, book: schemas.BookCreate, db: Session = Depends(database.get_db)):
    updated = crud.update_book(db, book_id, book)
    if not updated:
        raise HTTPException(status_code=404, detail="Book not found")
    return updated

@app.delete("/books/{book_id}")
def delete_book(book_id: int, db: Session = Depends(database.get_db)):
    if not crud.delete_book(db, book_id):
        raise HTTPException(status_code=404, detail="Book not found")
    return {"status": "deleted"}

@app.get("/")
async def serve_index():
    return FileResponse(os.path.join(os.path.dirname(__file__), "static/index.html"))