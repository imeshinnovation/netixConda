from fastapi import APIRouter, Depends
from controllers.movies import (
    find_all_movies,
    find_one_movie,
    add_movie,
    update_movie,
    delete_movie,
)
from models.user import UserDB
from controllers.user import (
    get_current_active_user
)
from models.movies import movieBase

movie = APIRouter()

@movie.post('/movies', tags=["Movies"])
async def create_movie(movie: movieBase, current_user: UserDB = Depends(get_current_active_user)):
    return await add_movie(movie)

@movie.get('/movies', tags=["Movies"])
async def get_all_movies(current_user: UserDB = Depends(get_current_active_user)):
    return await find_all_movies()

@movie.get('/movies/{id}', tags=["Movies"])
async def get_movie(id: str, current_user: UserDB = Depends(get_current_active_user)):
    return await find_one_movie(id)

@movie.put('/movies/{id}', tags=["Movies"])
async def put_movie(
    id: str, 
    movie: movieBase, 
    current_user: movieBase = Depends(get_current_active_user)
):
    return await update_movie(id, movie)

@movie.delete('/movies/{id}', tags=["Movies"])
async def remove_movie(
    id: str, 
    current_movie: movieBase = Depends(get_current_active_user)
):
    return await delete_movie(id)