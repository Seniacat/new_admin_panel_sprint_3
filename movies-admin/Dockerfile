FROM python:3.10

ARG APP_HOME=/opt/app
WORKDIR ${APP_HOME}

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV UWSGI_PROCESSES 1
ENV UWSGI_THREADS 16
ENV UWSGI_HARAKIRI 240
ENV DJANGO_SETTINGS_MODULE 'config.settings'

COPY entrypoint.sh entrypoint.sh
COPY fixtures.json fixtures.json
COPY requirements.txt requirements.txt
COPY uwsgi/uwsgi.ini uwsgi.ini

RUN  chmod +x 'entrypoint.sh' \
     && mkdir -p /opt/app/static/ \
     && pip install --upgrade pip \
     && pip install -r requirements.txt \
     && groupadd -r app && useradd -d ${APP_HOME} -r -g app app \
     && chown app:app -R ${APP_HOME}

COPY . .

EXPOSE 8000

USER app

ENTRYPOINT ["./entrypoint.sh"]
