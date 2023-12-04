from typing import Annotated

from fastapi import FastAPI, Depends, HTTPException, Path
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from starlette import status

from models import TodoList, Base
from database import engine, SessionLocal

app = FastAPI()

Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


@app.get("/")
async def read_all(db: db_dependency):
    return db.query(TodoList).all()


class TodoRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
    status: bool


@app.get("/todo/{todo_id}", status_code=status.HTTP_200_OK)
async def read_todo_by_id(db: db_dependency, todo_id: int = Path(gt=0)):
    todo_model = db.query(TodoList).filter(TodoList.id == todo_id).first()
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404, detail="Todo not found")


@app.post("/todo", status_code=status.HTTP_201_CREATED)
async def create_todo_list(todo: TodoRequest, db: db_dependency):
    todo_model = TodoList(**todo.dict())
    db.add(todo_model)
    db.commit()
