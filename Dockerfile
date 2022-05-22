FROM python:3.9
LABEL maintainer="meglomnic@hotmail.com"

COPY . /app/server
WORKDIR /app/server

RUN pip3 install -r requirements.txt

ENV STORAGE_TYPE=file \
    STORAGE_HOST= \
    STORAGE_PORT= \
    STORAGE_EXPIRE_SECONDS= \
    STORAGE_DB= \
    STORAGE_AWS_BUCKET= \
    STORAGE_AWS_REGION= \
    STORAGE_USENAMER= \
    STORAGE_PASSWORD= \
    STORAGE_FILEPATH= 

ENV HOST=0.0.0.0\
    PORT=7777\
    KEY_LENGTH=10\
    MAX_LENGTH=400000\
    STATIC_MAX_AGE=86400\
    RECOMPRESS_STATIC_ASSETS=true

ENV KEYGENERATOR_TYPE=phonetic \
    KEYGENERATOR_KEYSPACE=

ENV DOCUMENTS=about=./about.md

EXPOSE ${PORT}
STOPSIGNAL SIGINT

CMD ["uvicorn", "server:app", "--workers", "4"]
