FROM python:3.10

WORKDIR ./app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./app ./app

EXPOSE 8000

RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r ./app/requirements.txt
