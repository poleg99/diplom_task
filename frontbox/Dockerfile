FROM python:3.9.9-slim-buster
LABEL maintainer="Oleg Pavlov" version="0.1.0"

ENV NODE_ENV production
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV FLASK_ENV=development

RUN apt-get update  && apt-get -y install curl

COPY requirements.txt .

RUN pip install --upgrade pip -r requirements.txt

COPY . .

RUN useradd -m app
USER app

EXPOSE 3000
HEALTHCHECK CMD curl -f http://localhost:3000/ping || exit 1

CMD ["python", "front_api.py"]
