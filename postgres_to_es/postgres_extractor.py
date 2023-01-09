from datetime import datetime

import backoff

from config import backoff_config
from models import Movie
from pg_queries import (get_genre_updates, get_movies_updates,
                        get_person_updates)
from state import JsonFileStorage, State


class PostgresExtractor:
    """Класс для выгрузки данных из БД Postgres."""
    @backoff.on_exception(**backoff_config)
    def __init__(self, pg_conn, key: str):
        self.pg_conn = pg_conn
        self.cursor = self.pg_conn.cursor()
        self.batch_size = 100
        self.last_time = None
        self.key = key
        self.state = State(JsonFileStorage('./etl_state.json'))

    def get_query(self, load_from: str):
        """Формирует SQL запрос в Postgres в зависимости от
        таблицы, в которой проверяем обновления"""
        if self.key == 'person':
            return get_person_updates(load_from)
        elif self.key == 'genre':
            return get_genre_updates(load_from)
        return get_movies_updates(load_from)

    def _get_state(self):
        return self.state.get_state(self.key)

    def set_start_time(self):
        self.last_time = datetime.min
        self.state.set_state(self.key, str(self.last_time))
        return self.last_time

    @backoff.on_exception(**backoff_config)
    def extract_movies(self):
        """Получение пачки данных по фильмам."""
        state = self._get_state()
        if not state:
            state = self.set_start_time()
        movies_query = self.get_query(state)
        self.cursor.execute(movies_query)
        while table_rows := self.cursor.fetchmany(self.batch_size):
            for row in table_rows:
                yield Movie(**row), str(row['updated_at'])
