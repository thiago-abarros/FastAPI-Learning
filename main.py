from uuid import UUID
from typing import List
from fastapi import FastAPI, HTTPException

from models import User, Role, Gender, UserUpdateRequest

app = FastAPI()

db: List[User] = [
    User(
        id=UUID("0d191149-3fbd-4b87-a76f-87bbfa6c7efa"), 
        first_name = "João", 
        last_name = "Neto", 
        gender = Gender.male,
        roles = [
            Role.student,
            Role.admin
            ]
        ),
    User(
        id= UUID("9d2a827d-b0e9-41f3-9a9d-47bdbad88398"),
        first_name = "Alexa",
        last_name = "Jones",
        gender = Gender.female,
        roles = [
            Role.user
        ]
    )
]

@app.get("/")
async def root():
    return {"hello":"world"}

@app.get("/api/users")
async def fetch_users():
    return db

@app.post("/api/users")
async def create_user(user: User):
    db.append(user)
    return {"id": user.id}

@app.delete("/api/users/{user_id}")
async def delete_user(user_id: UUID):
    for user in db:
        if user.id == user_id:
            db.remove(user)
            return
    raise HTTPException(
        status_code=404,
        detail=f"User with id: {user_id} does not exists"
    )

@app.put("/api/users/{user_id}")      
async def update_user(user_update: UserUpdateRequest, user_id: UUID):
    for user in db:
        if user.id == user_id:
            if user_update.first_name is not None:
                user.first_name = user_update.first_name
            if user_update.last_name is not None:
                user.last_name = user_update.last_name
            if user_update.roles is not None:
                user.roles = user_update.roles
            return
        
    raise HTTPException(
        status_code=404,
        detail=f"User with id: {user_id} does not exists"
    )

            