FROM python:3-alpine

WORKDIR /usr/src/app

RUN apk upgrade && \
    apk add --no-cache postgresql-libs && \
    apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
    pip install Flask && \
    pip install psycopg2-binary && \
    pip install psycopg2 && \
    pip install pyjwt && \
    pip install bcrypt && \
    pip install requests && \
    pip install gunicorn && \
    pip install redis && \
    apk --purge del .build-deps

COPY . .

CMD ["gunicorn","-w", "2", "-b", "0.0.0.0:8000", "main:app"]

