from src.db.DBConnection import PostgreSQLConnection
from src.models.User import User

db = PostgreSQLConnection(dbname = 'postgres', user = 'pdeostgres', password = 'postgres', host = 'db', port = '5432')

async def c_get_user(user_id: int):
    db.connect()
    user = db.select_user(f"SELECT * FROM users WHERE id = {user_id}")
    db.close()
    return user

async def c_create_user(user: User):
    db.connect()
    db.insert_user(user.id, user.name, user.area, user.job_description, user.role, user.salary, user.is_active, user.last_evaluation)
    db.close()
    return user 

async def c_delete_user(user_id: int):
    db.connect()
    user = db.delete_user(user_id)
    db.close()
    return user 

async def c_update_user(user: User):
    db.connect()
    user = db.update_user(user.id, user.name, user.area, user.job_description, user.role, user.salary, user.is_active, user.last_evaluation)
    db.close()
    return user