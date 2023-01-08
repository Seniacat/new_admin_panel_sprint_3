import logging
import time
from dotenv import load_dotenv

from config import sleep_freq, index_file
from data_transform import transform
from elasticsearch_loader import ELasticSearchLoader
from postgres_extractor import PostgresExtractor


load_dotenv()


logger = logging.getLogger('ES_Loader')


def loader(key: str):
    """Основной метод загрузки данных из Postgres в Elasticsearch"""
    logger.info(
        f'PostgreSQL connection is open. Start loading data from {key}'
    )
    postgres_extractor = PostgresExtractor(key)
    es_loader = ELasticSearchLoader(key)
    if not es_loader.index_exist(es_loader.index):
        es_loader.create_index(index_file)
        logger.info(f'Created index {es_loader.index}')
    data = postgres_extractor.extract_movies()
    es_data = transform(data)
    es_loader.bulk_load(es_data)


if __name__ == '__main__':

    while True:
        for table in ['movies', 'person', 'genre']:
            loader(table)
            time.sleep(5)

        logger.info(f'Sleep for {sleep_freq} seconds')
        time.sleep(sleep_freq)
