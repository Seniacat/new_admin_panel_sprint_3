import json
from typing import Iterator, Tuple

import backoff
from elasticsearch import Elasticsearch, helpers

from config import backoff_config, es_conf
from logger import logger
from state import JsonFileStorage, State


class ELasticSearchLoader:
    """Класс для загрузки данных в Elasticsearch."""
    @backoff.on_exception(**backoff_config)
    def __init__(self) -> None:
        self.conf = es_conf
        self.index = 'movies'
        self.batch_size = 100
        self.last_time = None
        self.state = State(JsonFileStorage('./etl_state.json'))
        self.connection = self._create_connection()

    @backoff.on_exception(**backoff_config)
    def _create_connection(self) -> Elasticsearch:
        """Создание подключения для Elasticsearch."""
        return Elasticsearch([f"{self.conf.host}:{self.conf.port}"])

    @backoff.on_exception(**backoff_config)
    def create_index(self, file_path: str) -> None:
        """Создание индекса в Elasticsearch."""
        with open(file_path, 'r') as file:
            f = json.load(file)
            self.connection.indices.create(index=self.index, body=f)
            return self.connection.indices.get(index=self.index)

    @backoff.on_exception(**backoff_config)
    def index_exist(self, index: str):
        """Проверка существования индекса в Elasticsearch."""
        return self.connection.indices.exists(index=self.index)

    def generate_docs(
        self, data: Iterator[Tuple[dict, str]], key: str
    ) -> Iterator[dict]:
        count = 0
        for film, updated_at in data:
            count += 1
            self.last_time = updated_at

            yield film

            if count % self.batch_size == 0:
                self.state.set_state(key, self.last_time)

        if self.last_time:
            self.state.set_state(key, self.last_time)

    @backoff.on_exception(**backoff_config)
    def bulk_load(self, data, key) -> None:
        """ Загрузка в Elasticsearch подготовленных данных
        пачками размера batch_sise и запись в состояние
        времени последней строки
        """

        docs_generator = self.generate_docs(data, key)

        success, failed = helpers.bulk(
            client=self.connection,
            actions=docs_generator,
            index=self.index,
            chunk_size=self.batch_size
        )

        if success == 0:
            logger.info('Nothing to update yet')
        else:
            logger.info(f'{success} items saved for index movies')
