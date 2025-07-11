from fastapi import APIRouter, Depends
from controllers.user import (
    find_all_users,
    find_one_user,
    add_user,
    update_user,
    delete_user,
    login_user,
    get_current_active_user
)
from models.user import UserCreate, UserUpdate, UserLogin, UserDB

user = APIRouter()

@user.post("/login", tags=["Authenticate"])
async def login_for_access_token(user_data: UserLogin):
    return await login_user(user_data)

@user.post('/users', tags=["Users"])
async def create_user(user: UserCreate):
    return await add_user(user)

@user.get('/users', tags=["Users"])
async def get_all_users(current_user: UserDB = Depends(get_current_active_user)):
    return await find_all_users()

@user.get('/users/{id}', tags=["Users"])
async def get_user(id: str, current_user: UserDB = Depends(get_current_active_user)):
    return await find_one_user(id)

@user.put('/users/{id}', tags=["Users"])
async def put_user(
    id: str, 
    user: UserUpdate, 
    current_user: UserDB = Depends(get_current_active_user)
):
    return await update_user(id, user)

@user.delete('/users/{id}', tags=["Users"])
async def remove_user(
    id: str, 
    current_user: UserDB = Depends(get_current_active_user)
):
    return await delete_user(id)