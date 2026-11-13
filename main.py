from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from typing import List
git commit -m "Добавил обработку ошибок для фильмов"
app = FastAPI()


class MovieCreate(BaseModel):
    title: str = Field(..., min_length=2, description="Название фильма")
    director: str = Field(..., min_length=2, description="Кто снял фильм")
    year: int = Field(..., ge=1900, le=2030, description="Год выпуска")


class Movie(MovieCreate):
    id: int

movies = [
    {"id": 1, "title": "Интерстеллар", "director": "Кристофер Нолан", "year": 2014},
    {"id": 2, "title": "Матрица", "director": "Лана и Лилли Вачовски", "year": 1999},
]


@app.get("/movies", response_model=List[Movie], status_code=status.HTTP_200_OK)
def get_movies():
    return movies

@app.get("/movies/{movie_id}", response_model=Movie)
def get_movie(movie_id: int):
    for movie in movies:
        if movie["id"] == movie_id:
            return movie
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Фильм с ID {movie_id}  не найден"
    )

@app.post("/movies", response_model=Movie, status_code=status.HTTP_201_CREATED)
def create_movie(movie_in: MovieCreate):
    for existing_movie in movies:
        if existing_movie["title"].lower() == movie_in.title.lower():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Фильм '{movie_in.title}' уже есть в базе"
            )
    new_id = movies[-1]["id"] + 1 if movies else 1
    new_movie = {"id": new_id, **movie_in.model_dump()}
    movies.append(new_movie)

    return new_movie
