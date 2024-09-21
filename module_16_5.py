# Домашнее задание по теме "Шаблонизатор Jinja 2." Цель: научиться взаимодействовать с шаблонами
# Jinja 2 и использовать их в запросах.

from fastapi import FastAPI, Path, status, Body, HTTPException, Request
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import Annotated, List

app = FastAPI()

users = []

templates = Jinja2Templates(directory="templates")

class User(BaseModel):
    id: int = None
    username: str
    age: int

@app.get("/")
async def read_users(request: Request):
    return templates.TemplateResponse("users.html", {"request": request, "users": users})


@app.get("/users/{user_id}")
async def read_user(request: Request, user_id: Annotated[int, Path()]):
    for user in users:
        if user.id == user_id:
            return templates.TemplateResponse("users.html", {"request": request, "user": user})
    raise HTTPException(status_code=404, detail="User not found")

@app.post("/user/{username}/{age}")
async def create_user(
    username: Annotated[str, Path(min_length=5, max_length=20, description="Введите имя пользователя")],
    age: Annotated[int, Path(ge=18, le=120, description="Введите возраст")]):
    user_id = 1 if not users else users[-1].id + 1
    user = User(id=user_id, username=username, age=age)
    users.append(user)
    return user

@app.put("/user/{user_id}/{username}/{age}")
async def update_user(
    user_id: Annotated[int, Path()],
    username: Annotated[str, Path(min_length=5, max_length=20, description="Введите имя пользователя")],
    age: Annotated[int, Path(ge=18, le=120, description="Введите возраст")]):
    for user in users:
        if user.id == user_id:
            user.username = username
            user.age = age
            return user
    raise HTTPException(status_code=404, detail="User was not found")

@app.delete("/user/{user_id}")
async def delete_user(user_id: Annotated[int, Path()]):
    for ind, user in enumerate(users):
        if user.id == user_id:
            deleted_user = users.pop(ind)
            return deleted_user
    raise HTTPException(status_code=404, detail="User was not found")