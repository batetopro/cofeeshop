FROM python:3.8-alpine

RUN apk add --no-cache --virtual .build-deps gcc postgresql-dev musl-dev python3-dev
RUN apk add libpq

COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt

RUN apk del --no-cache .build-deps


RUN mkdir -p /coffeeshop
COPY config.py /coffeeshop/
COPY coffeeshop.py /coffeeshop/
RUN mkdir -p /coffeeshop/assets
COPY assets/dataset.zip /coffeeshop/assets
RUN mkdir -p /coffeeshop/api
COPY api/ /coffeeshop/api/
RUN mkdir -p /coffeeshop/loader
COPY loader/ /coffeeshop/loader/


WORKDIR /coffeeshop
ENV FLASK_APP=/coffeeshop/coffeeshop.py FLASK_DEBUG=1 PYTHONUNBUFFERED=
RUN flask db init && flask db migrate -m "Make migrations."
CMD sleep 5 && flask db upgrade && flask load_data && uvicorn api.main:app --host 0.0.0.0 --port 80
