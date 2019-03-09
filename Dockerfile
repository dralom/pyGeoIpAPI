FROM python:3.7-slim

RUN apt-get clean \
    && apt-get -y update

RUN apt-get -y install nginx \
    && apt-get -y install build-essential

COPY ./template /
COPY ./src /Main/pyGeoIpAPI

WORKDIR /Main/pyGeoIpAPI

RUN pip install uwsgi
RUN pip install -r requirements.txt --src /usr/local/src

RUN mkdir logs

RUN python update.py

RUN chown -R www-data:www-data /Main

RUN chmod u+x ./start.sh

CMD ["./start.sh"]
