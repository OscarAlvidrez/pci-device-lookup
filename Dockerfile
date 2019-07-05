FROM python:3.7-alpine3.8

WORKDIR /usr/src/app

COPY loader/requirements.txt ./

RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

RUN pip install --no-cache-dir -r requirements.txt

COPY ./loader .

CMD [ "python", "./loaddb.py" ]