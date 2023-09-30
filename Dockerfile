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
    apk --purge del .build-deps

COPY . .

CMD ["python3", "main.py"]

