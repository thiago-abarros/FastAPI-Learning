from uuid import UUID
from typing import List
from fastapi import FastAPI, HTTPException, Response

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
    """
    Root endpoint for the API.
    Returns:
        dict: A simple message indicating the API is running.
    """
    return {"hello":"world"}

@app.get("/api/users")
async def fetch_users() -> List[User]:
    """
    Function to fetch users from the API endpoint "/api/users".

    This is an asynchronous function with no parameters and it returns the 'db' object,
    which is a list of User objects.

    Returns:
        List[User]: A list of User objects representing the users in the database.
    """
    return db

@app.post("/api/users")
async def create_user(user: User):
    """
    Create a new user by adding the user object to the database
    and return the user's id.

    Parameters:
        user (User): The user object to be added to the database.

    Returns:
        dict: A dictionary containing the user's id.
    """
    db.append(user) 
    return {"id": user.id} 

@app.delete("/api/users/{user_id}")
async def delete_user(user_id: UUID):
    """
    Delete a user from the database by user ID.

    This function is an asynchronous function that deletes a user from the
    database based on the user ID. The function takes a UUID as a parameter
    and returns None. If the user is not found in the database, a 404 NOT
    FOUND status code with a message indicating that the user does not
    exist is returned.

    Parameters:
    - user_id (UUID): The unique identifier of the user to be deleted.

    Returns:
    - None
    """

    try:
        user_id_obj = UUID(str(user_id))
    except ValueError:
        raise HTTPException(
            status_code=422,
            detail="%s is not a valid UUID" % user_id
        )

    user = next((user for user in db if user.id == user_id_obj), None)
    if user:
        db.remove(user)
        return Response(status_code=200)
    else:
        raise HTTPException(
            status_code=404,
            detail="User with id: %s does not exist" % user_id
        )

@app.put("/api/users/{user_id}")
async def update_user(user_update: UserUpdateRequest, user_id: UUID):
    """
    Update a user's information in the database.

    This function updates a user's information in the database based on the
    user_id. The function takes a UserUpdateRequest object which has the
    updated information for the user. The function returns a 200 status code
    upon success and a 404 status code if the user is not found in the
    database.

    Parameters:
        user_update (UserUpdateRequest): The user update request object.
        user_id (UUID): The unique identifier of the user to be updated.
    """
    user_index = next((i for i, user in enumerate(db) if user.id == user_id), None)
    if user_index is not None:
        user = db[user_index]
        fields = user_update.model_dump(exclude_unset=True)
        user.__dict__.update(fields)
    else:
        raise HTTPException(status_code=404)
