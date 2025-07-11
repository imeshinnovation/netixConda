from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from jose import JWTError, jwt
from config.db import conn
from schemas.user import userEntity, usersEntity
from models.user import UserCreate, UserDB, UserUpdate, UserLogin
from helpers.secure import hash_password, verify_password
from typing import Optional
from bson import ObjectId
from bson.errors import InvalidId
from datetime import datetime
from config.security import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login",
                                     scheme_name="Bearer",
                                     auto_error=True)


async def find_all_users():
    users = await conn.user.find({}).to_list(length=None)
    return usersEntity(users)


async def find_one_user(id: str):
    try:
        user = await conn.user.find_one({"_id": ObjectId(id)})
        if not user:
            raise HTTPException(status_code=404, detail="The ID does not exist")
        return userEntity(user)
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid ID")


async def add_user(user: UserCreate):
    existing_user = await conn.user.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The email is already registered"
        )
    hashed_password = hash_password(user.password)
    user_db = UserDB(
        **user.model_dump(exclude={"password"}),
        password=hashed_password
    ).model_dump()
    result = await conn.user.insert_one(user_db)
    user_db["id"] = str(result.inserted_id)
    return UserDB(**user_db)


async def update_user(id: str, user: UserUpdate):
    try:
        obj_id = ObjectId(id)
        existing_user = await conn.user.find_one({"_id": obj_id})
        if not existing_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="The ID does not exist"
            )
        update_data = user.model_dump(exclude_unset=True)
        if "password" in update_data:
            hashed_password = hash_password(update_data["password"])
            update_data["password"] = hashed_password
        if "email" in update_data:
            if await conn.user.find_one({"email": update_data["email"], "_id": {"$ne": obj_id}}):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="The email is already in use"
                )
        update_data["updated_at"] = datetime.utcnow()
        result = await conn.user.update_one(
            {"_id": obj_id},
            {"$set": update_data}
        )
        if result.modified_count == 1:
            raise HTTPException(
                    status_code=status.HTTP_200_OK,
                    detail="User updated successfully"
                )
        else:
            raise HTTPException(
                status_code=status.HTTP_304_NOT_MODIFIED,
                detail="No changes were made"
            )
    except InvalidId:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid ID"
        )


async def delete_user(id: str):
    try:
        obj_id = ObjectId(id)
        existing_user = await conn.user.find_one({"_id": obj_id})
        if not existing_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="The ID does not exist"
            )
        await conn.user.delete_one({"_id": obj_id})
        raise HTTPException(
            status_code=status.HTTP_200_OK,
            detail="Record Deleted"
        )
    except InvalidId:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid ID format"
        )


async def authenticate_user(email: str, password: str):
    user = await conn.user.find_one({"email": email})
    if not user:
        return None
    if not verify_password(password, user["password"]):
        return None
    return user


async def login_user(user_login: UserLogin):
    user = await authenticate_user(user_login.email, user_login.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=int(ACCESS_TOKEN_EXPIRE))
    access_token = create_access_token(
        data={"sub": str(user["_id"]), "email": user["email"]},
        expires_delta=access_token_expires
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": userEntity(user)
    }


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credentials could not be validated",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    try:
        user = await find_one_user(user_id)
        if user is None:
            raise credentials_exception
        return user
    except InvalidId:
        raise credentials_exception



async def get_current_active_user(current_user: dict = Depends(get_current_user)):
    if current_user.get("disabled", False):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    return current_user