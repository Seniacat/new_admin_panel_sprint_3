# Заключительное задание первого модуля

Ваша задача в этом уроке — загрузить данные в Elasticsearch из PostgreSQL. Подробности задания в папке `etl`.

## Запуск проекта в контейнере
Клонируйте репозиторий и перейдите в директорию new_admin_panel_sprint_3:
```
git clone https://github.com/Seniacat/new_admin_panel_sprint_3
cd new_admin_panel_sprint_3/
```
Создайте и заполните .env файл с переменными окружения по примеру env.example:
```
echo SECRET_KEY=xxxxx >> .env

echo DB_ENGINE=django.db.backends.postgresql >> .env

echo DB_NAME=postgres >> .env

echo POSTGRES_PASSWORD=postgres >> .env

echo POSTGRES_USER=postgres  >> .env

echo DB_HOST=db  >> .env

echo DB_PORT=5432  >> .env

echo ELASTICSEARCH_HOST  >> .env

echo ELASTICSEARCH_PORT=9200  >> .env
```
Установите и запустите приложения в контейнерах командой:
```
docker-compose up -d
```
В контейнерах запустятся сервисы - Postgres, movies_admin, nginx, ElasticSearch, ETL

Сервис ETL проверяет наличие обновлений в базе каждые 5 минут.
