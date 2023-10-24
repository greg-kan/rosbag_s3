from pathlib import Path
import json
from datetime import date
import os

CONF_APP_FILE = 'conf.json'
APP_FOLDER = '.rosbag_processor'

app_home = Path.home() / APP_FOLDER
if not os.path.exists(app_home):
    raise Exception(f"Util home folder absent: {app_home}")

app_conf_file = app_home / CONF_APP_FILE

try:
    with open(app_conf_file) as f_json:
        data_json = json.load(f_json)

    bag_file_extension = data_json['bag_file_extension']
    log_file = app_home / f"{data_json['log_file']}_{date.today()}.log"
except Exception:
    raise Exception(f"Config file absent or wrong format: {app_conf_file}")