FROM python:3.11.1-buster
ENV PYTHONUNBUFFERED 1
RUN mkdir -p /opt/app
WORKDIR /opt/app
COPY ./project/ .
COPY ./requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
VOLUME /opt/app
EXPOSE 8000
CMD python manage.py makemigrations && python manage.py migrate && python manage.py runserver 0.0.0.0:8000