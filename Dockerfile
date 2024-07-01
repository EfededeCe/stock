### El Dockerfile se hizo siguiendo la siguiente guia:
# https://testdriven.io/blog/dockerizing-django-with-postgres-gunicorn-and-nginx/
# https://testdriven.io/blog/docker-best-practices/

# pull official base image
FROM python:3.11.4-slim-buster

# set work directory
WORKDIR /usr/src/stock

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install system dependencies
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
  gcc \
  python3-dev \
  default-libmysqlclient-dev \
  pkg-config \
  netcat \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt


# copy entrypoint.sh
COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g' /usr/src/stock/entrypoint.sh
RUN chmod +x /usr/src/stock/entrypoint.sh

# copy project
COPY . .

# run entrypoint.sh
ENTRYPOINT ["/usr/src/stock/entrypoint.sh"]








#### En desuso ###
# FROM python:3.10
# WORKDIR /usr/src/app
# COPY ./requirements.txt .
# RUN pip install -r requirements.txt
# COPY ./ /app
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
