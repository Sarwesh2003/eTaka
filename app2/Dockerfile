FROM python:3

COPY ./requirements.txt /requirements.txt

WORKDIR /

RUN pip install -r requirements.txt

COPY . /


CMD gunicorn -w 4 --bind 0.0.0.0:5000 app2:app2
