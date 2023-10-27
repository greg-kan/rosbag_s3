from pathlib import Path
import json
from datetime import date
import os

APP_FOLDER = '.rosbag_processor'
CONF_APP_FILE = 'conf.json'
CONF_CONNECTION_FILE = 'connect.json'

app_home = Path.home() / APP_FOLDER

if not os.path.exists(app_home):
    raise Exception(f"Util home folder absent: {app_home}")

app_conf_file = app_home / CONF_APP_FILE
connect_conf_file = app_home / CONF_CONNECTION_FILE

try:
    with open(app_conf_file) as f_json:
        data_json = json.load(f_json)

    bag_file_extension = data_json['bag_file_extension']
    log_file = app_home / f"{data_json['log_file']}_{date.today()}.log"
except Exception:
    raise Exception(f"Config file absent or wrong format: {app_conf_file}")

try:
    with open(connect_conf_file) as f_json:
        data_json = json.load(f_json)

    s3_url = data_json['url']
    s3_accessKey = data_json['accessKey']
    s3_secretKey = data_json['secretKey']
    s3_api = data_json['api']
    s3_path = data_json['path']
except Exception:
    raise Exception(f"Config file absent or wrong format: {connect_conf_file}")
