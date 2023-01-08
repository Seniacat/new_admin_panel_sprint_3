FROM python:3.10

WORKDIR /etl

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt /etl
RUN pip install --upgrade pip \
    && pip install -r /etl/requirements.txt --no-cache-dir

COPY . /etl

EXPOSE 8000

CMD python /etl/load_to_es.py