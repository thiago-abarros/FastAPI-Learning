from fastapi import FastAPI, HTTPException

from src.controller.UserController import c_create_user, c_delete_user, c_get_user, c_update_user
from src.models.User import User 

app = FastAPI

userNotFound = "O usuário não existe"

@app.get("/users")
async def get_user(user_id: int):
    db_user = await c_get_user(user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail=userNotFound)
    return db_user

@app.post("/users")
async def create_user(user: User):
    db_user = await c_get_user(user)
    if db_user:
        raise HTTPException(status_code=404, detail="O usuário já existe")
    user = await c_create_user(user)

    return user

@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    db_user = await c_delete_user(user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail=userNotFound)
    return db_user

@app.put("/users/{user_id}")
async def update_user(user: User):
    db_user = await c_update_user(user)
    if db_user is None:
        raise HTTPException(status_code=404, detail=userNotFound)
    return db_user