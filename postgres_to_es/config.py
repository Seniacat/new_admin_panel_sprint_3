import backoff
from pydantic import BaseSettings, Field

from logger import logger


class PostgresConfig(BaseSettings):
    dbname: str = Field(..., env='DB_NAME')
    user: str = Field(..., env='POSTGRES_USER')
    password: str = Field(..., env='POSTGRES_PASSWORD')
    host: str = Field(..., env='DB_HOST')
    port: int = Field(..., env='DB_PORT')


class ES_Config(BaseSettings):
    host: str = Field(..., env='ELASTICSEARCH_HOST')
    port: str = Field(..., env='ELASTICSEARCH_PORT')


backoff_config = {
    'wait_gen': backoff.expo,
    'exception': Exception,
    'max_tries': 3600,
    'raise_on_giveup': False,
    'logger': logger
}

index_file = './indexes/movies.json'

sleep_freq = 300

postgres_dsn = PostgresConfig()
es_conf = ES_Config()
