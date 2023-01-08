from typing import List, Optional, Union
from uuid import UUID

from pydantic import BaseModel


class UUIDModel(BaseModel):
    id: UUID


class Person(UUIDModel):
    name: str


class Genre(UUIDModel):
    name: str


class Movie(UUIDModel):
    imdb_rating: Optional[float]
    genre: Union[List[str], str]
    title: str
    description: Optional[str]
    actors: Optional[List[Person]]
    writers: Optional[List[Person]]
    director: Optional[List[Person]]
    actors_names: Optional[List[str]]
    writers_names: Optional[List[str]]
