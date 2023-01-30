FROM python:latest
WORKDIR /code
COPY ./django-shop /code/
RUN pip install -r requirements.txt
EXPOSE 8000