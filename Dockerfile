FROM python:alpine

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app
COPY . .

# install updates and necessary modules
RUN apk update -qq && apk add libpq
RUN apk add --no-cache curl git build-base automake libtool
RUN apk add --virtual .build-deps gcc python3-dev musl-dev postgresql-dev

# update pip python
RUN pip3 install -U pip

# install packages for the project
RUN pip3 install -r requirements.txt

# remove build dependencies
RUN apk del .build-deps
