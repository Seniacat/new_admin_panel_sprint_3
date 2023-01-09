from uuid import UUID

from pydantic import BaseModel


class UUIDModel(BaseModel):
    id: UUID


class Person(UUIDModel):
    name: str


class Genre(UUIDModel):
    name: str


class Movie(UUIDModel):
    imdb_rating: float | None
    genre: list[str] | str
    title: str
    description: str | None
    actors: list[Person] | None
    writers: list[Person] | None
    director: list[Person] | None
    actors_names: list[str] | None
    writers_names: list[str] | None
