import os
import shutil
import tarfile
import logging.config

import requests

from config import *
from utils import compute_md5

lg = logging.getLogger(__name__)


def check_md5(db_archive_name, db_path):
    lg.debug("Checking MD5 for {} located at {}".format(db_archive_name, db_path))
    db_name = geolite2_databases_archive_name[db_archive_name]
    md5_url = geolite2_databases_url_md5[geolite2_databases_name_url[db_name]]
    online_md5 = requests.get(md5_url, allow_redirects=True).text
    lg.debug("Online MD5 is: {}".format(online_md5))
    if os.path.isfile(db_path):
        local_md5 = compute_md5(db_path)
        lg.debug("Local MD5 is: {}".format(local_md5))
    else:
        raise Exception("Database file does not exist: {}".format(db_path))
    return online_md5 == local_md5


def unpack_db(db_name, db_archive_name, temp_file_path, db_path):
    lg.debug("Unpacking archive: {}".format(temp_file_path))
    tf = tarfile.open(temp_file_path)
    db_tar_file_path = ""
    db_name = geolite2_databases_archive_name[db_archive_name]
    temp_folder = os.path.join(os.getcwd(), "temp")
    lg.debug("Creating temporary folder {}".format(temp_folder))
    os.makedirs(temp_folder)
    for member in tf.getmembers():
        if db_name in member.path:
            db_tar_file_path = member.path
            lg.debug("Identified database file in tar file at path: {}".format(db_tar_file_path))
            break

    if db_tar_file_path is "":
        exception_message = "Could not find database {} in file {}".format(db_name, temp_file_path)
        lg.exception(exception_message)
        raise Exception(exception_message)
    else:
        lg.debug("Extracting {} to {}".format(db_tar_file_path, temp_folder))
        tf.extract(db_tar_file_path, path=temp_folder)
        tf.close()

    file_moved = False
    for root, subdirs, files in os.walk(temp_folder):
        for file in files:
            if file == db_name:
                tpath = os.path.join(root, file)
                shutil.move(tpath, db_path)
                lg.debug("Moved file from {} to {}".format(tpath, db_path))
                file_moved = True
                break

    if not file_moved:
        exception_message = "Could not move file {}".format(db_name)
        lg.exception(exception_message)
        raise Exception(exception_message)

    lg.debug("Deleting {}".format(temp_folder))
    shutil.rmtree(temp_folder, ignore_errors=True)
    lg.debug("Deleted {}".format(temp_folder))
    return True


def download_db(db_archive_name, db_archive_path):
    lg.debug("Initiating download of {} into {}".format(db_archive_name, db_archive_path))
    db_name = geolite2_databases_archive_name[db_archive_name]
    db_path = os.path.join(os.getcwd(), db_name)
    db_url = geolite2_databases_name_url[db_name]
    temp_file_name = db_url[db_url.rfind("/") + 1:]
    temp_file_path = os.path.join(os.getcwd(), temp_file_name)

    lg.debug("Downloading from {}".format(db_url))
    r = requests.get(db_url, allow_redirects=True)
    with open(temp_file_path, 'wb') as f:
        lg.debug("Writing file {}".format(temp_file_path))
        f.write(r.content)
    if check_md5(db_archive_name, temp_file_path):
        unpack_db(db_name=db_name,
                  db_path=db_path,
                  db_archive_name=db_archive_name,
                  temp_file_path=temp_file_path, )
        # os.remove(temp_file_path)
    else:
        exception_message = "Could not validate downloaded file {} from {}".format(db_archive_name, db_url)
        lg.exception(exception_message)
        raise Exception(exception_message)


def update_database():
    lg.debug("Checking databases for updates.")
    for db_archive_file_name in geolite2_databases_archive_name.keys():
        db_archive_file_path = os.path.join(os.getcwd(), db_archive_file_name)
        if os.path.isfile(db_archive_file_path):  # database file exists
            if not check_md5(db_archive_file_name, db_archive_file_path):  # check if it is up to date
                lg.debug("File {} exists but the MD5 does not match the online MD5.".format(db_archive_file_path))
                download_db(db_archive_file_name, db_archive_file_path)  # it is not up to date, download updated file
        else:  # database file does not exist
            lg.debug("File {} does not exists. Will download it.".format(db_archive_file_name))
            download_db(db_archive_file_name, db_archive_file_path)  # download it


if __name__ == "__main__":
    logging.config.fileConfig('logging.conf', disable_existing_loggers=False)
    update_database()
