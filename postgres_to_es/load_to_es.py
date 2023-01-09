import time
from contextlib import closing

import psycopg2
from psycopg2.extras import DictCursor

from config import index_file, postgres_dsn, sleep_freq
from data_transform import transform
from elasticsearch_loader import ELasticSearchLoader
from logger import logger
from postgres_extractor import PostgresExtractor


def loader(pg_conn, key: str):
    """Основной метод загрузки данных из Postgres в Elasticsearch"""
    logger.info(
        f'PostgreSQL connection is open. Start loading data from {key}'
    )
    postgres_extractor = PostgresExtractor(pg_conn, key)
    data = postgres_extractor.extract_movies()
    es_data = transform(data)
    es_loader.bulk_load(es_data, key)


if __name__ == '__main__':

    es_loader = ELasticSearchLoader()
    if not es_loader.index_exist(es_loader.index):
        es_loader.create_index(index_file)
        logger.info(f'Created index {es_loader.index}')

    while True:
        with closing(
            psycopg2.connect(**postgres_dsn.dict(), cursor_factory=DictCursor)
        ) as pg_conn:
            for table in ['movies', 'person', 'genre']:
                loader(pg_conn, table)
                time.sleep(5)

        logger.info(f'Sleep for {sleep_freq} seconds')
        time.sleep(sleep_freq)
