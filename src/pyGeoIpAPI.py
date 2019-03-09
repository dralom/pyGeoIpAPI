import logging.config
import os

import geoip2.database
from flask import Flask

import update
from config import *

logging.config.fileConfig('logging.conf', disable_existing_loggers=False)

db_country_path = os.path.join(os.getcwd(), geolite2_country_name)
db_city_path = os.path.join(os.getcwd(), geolite2_city_name)
db_asn_path = os.path.join(os.getcwd(), geolite2_asn_name)

readerCountry = geoip2.database.Reader(db_country_path)
readerCity = geoip2.database.Reader(db_city_path)
readerASN = geoip2.database.Reader(db_asn_path)

app = Flask(__name__)


@app.route('/txt/update', methods=['GET'])
def update_databases():
    if update.update_database():
        return "Update successful"
    else:
        return "Update failed"


@app.route('/txt/country/name/<ip>', methods=['GET'])
def get_country_name_txt(ip):
    response = readerCountry.country(ip)
    return response.country.name


@app.route('/txt/country/code/<ip>', methods=['GET'])
def get_country_code_txt(ip):
    response = readerCountry.country(ip)
    return response.country.iso_code


@app.errorhandler(404)
def page_not_found_handler(e):
    return "404 Not Found"


@app.errorhandler(ValueError)
def value_error_handler(e):
    return "ERROR: Invalid value provided"


@app.errorhandler(Exception)
def generic_exception_handler(e):
    return e


if __name__ == "__main__":
    update.update_database()
    app.run(debug=False)
