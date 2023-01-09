from typing import Iterator

from models import Movie, Person


def get_names(persons: list[Person] | None):
    return [Person.name for Person in persons] if persons else []


def transform(data: Iterator[Movie]):
    """Преобразование полученных данных из Postgres
    в формат, пригодный для записи в Elasticsearch."""
    for film, last_time in data:
        if not film.actors:
            film.actors = []
        if not film.writers:
            film.writers = []
        film.actors_names = get_names(film.actors)
        film.writers_names = get_names(film.writers)
        film.director = get_names(film.director)
        instance = film.dict()
        instance['_id'] = instance['id']
        yield instance, last_time
