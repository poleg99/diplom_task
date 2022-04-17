FROM python:3.9.9-slim-buster
LABEL maintainer="Oleg Pavlov oleg.a.pavlov@gmail.com, version=0.1.0"

ENV NODE_ENV production
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV FLASK_ENV=development
ENV FLASK_APP=back_api.py

RUN apt-get update  && apt-get -y install curl
RUN apt-get install python3-dev default-libmysqlclient-dev gcc  -y

COPY requirements.txt .

RUN pip install --upgrade pip -r requirements.txt

COPY . .

RUN chmod +x /entrypoint.sh

RUN useradd -m app
RUN mkdir -p /migrations/versions
RUN chown -R app migrations
USER app

EXPOSE 8000
HEALTHCHECK CMD curl -f http://localhost:8000/ping || exit 1

ENTRYPOINT ["/entrypoint.sh"]
