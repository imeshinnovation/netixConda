from fastapi import HTTPException, status, Depends
from config.db import conn
from schemas.movies import movieEntity, moviesEntity
from models.movies import movieDB, movieBase
from bson import ObjectId
from bson.errors import InvalidId
from datetime import datetime

async def find_all_movies():
    movies = await conn.movies.find({}).to_list(length=None)
    return moviesEntity(movies)


async def find_one_movie(id: str):
    try:
        movie = await conn.movies.find_one({"_id": ObjectId(id)})
        if not movie:
            raise HTTPException(status_code=404, detail="The ID does not exist")
        return movieEntity(movie)
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid ID")


async def add_movie(movie: movieBase):
    existing_movie = await conn.movies.find_one({"uri": movie.uri})
    if existing_movie:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The movie is already registered"
        )
    movie_db = movieDB(
        **movie.model_dump()
    ).model_dump()
    result = await conn.movies.insert_one(movie_db)
    movie_db["id"] = str(result.inserted_id)
    return movieDB(**movie_db)


async def update_movie(id: str, movie: movieBase):
    try:
        obj_id = ObjectId(id)
        existing_movie = await conn.movies.find_one({"_id": obj_id})
        if not existing_movie:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="The ID does not exist"
            )
        update_data = movie.model_dump(exclude_unset=True)
        if "uri" in update_data:
            if await conn.movies.find_one({"uri": update_data["uri"], "_id": {"$ne": obj_id}}):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="The movie is already in use"
                )
        update_data["updated_at"] = datetime.utcnow()
        result = await conn.movies.update_one(
            {"_id": obj_id},
            {"$set": update_data}
        )
        if result.modified_count == 1:
            raise HTTPException(
                    status_code=status.HTTP_200_OK,
                    detail="Movie updated successfully"
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


async def delete_movie(id: str):
    try:
        obj_id = ObjectId(id)
        existing_movie = await conn.movies.find_one({"_id": obj_id})
        if not existing_movie:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="The ID does not exist"
            )
        await conn.movies.delete_one({"_id": obj_id})
        raise HTTPException(
            status_code=status.HTTP_200_OK,
            detail="Record Deleted"
        )
    except InvalidId:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid ID format"
        )

