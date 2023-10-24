from rosbag_processor import parser as pr
from pathlib import Path
import logging
from datetime import date


LOCAL_BAG_FILES_PATH = '/data1/s3/bg'
LOCAL_PICTURES_DESTINATION = '/data1/s3/pictures'
TOPICS = ['/realsense_gripper/aligned_depth_to_color/image_raw', '/realsense_gripper/color/image_raw/compressed']
MIN_FILTER_TIME = '2023-08-22 18:33:48'
MAX_FILTER_TIME = '2023-08-22 18:33:52'

APP_FOLDER = '.rosbag_processor'

path_to_files = LOCAL_BAG_FILES_PATH
path_to_pictures = LOCAL_PICTURES_DESTINATION
app_home = Path.home() / APP_FOLDER
app_log_file = app_home / f"{'rosbag_tester'}_{date.today()}.log"


def setup_logger(pname, plog_file, log_level=logging.INFO):
    handler = logging.FileHandler(plog_file)
    handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s'))

    vlogger = logging.getLogger(pname)
    vlogger.setLevel(log_level)
    vlogger.addHandler(handler)

    return vlogger


logger = setup_logger('application_logger', app_log_file)


def start_routine():
    logger.info("Routine started")
    pr.pars_files(path_to_files, path_to_pictures, topics=TOPICS,
                  start_time=MIN_FILTER_TIME, end_time=MAX_FILTER_TIME)
    logger.info("Routine finished")


if __name__ == "__main__":
    start_routine()
