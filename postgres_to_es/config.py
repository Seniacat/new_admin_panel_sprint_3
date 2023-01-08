import logging
import os

import backoff
from dotenv import load_dotenv

load_dotenv()


logger = logging.getLogger('ES_Loader')
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


dsl = {
    'dbname': os.getenv('DB_NAME'),
    'user': os.getenv('POSTGRES_USER'),
    'password': os.getenv('POSTGRES_PASSWORD'),
    'host': os.environ.get('DB_HOST'),
    'port': os.environ.get('DB_PORT'),
}

es_conf = [{
    'host': os.getenv('ELASTICSEARCH_HOST'),
    'port': os.getenv('ELASTICSEARCH_PORT'),
}]

backoff_config = {
    'wait_gen': backoff.expo,
    'exception': Exception,
    'max_tries': 3600,
    'raise_on_giveup': False,
    'logger': logger
}

index_file = './indexes/movies.json'

sleep_freq = 300
