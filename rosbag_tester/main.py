from rosbag_processor import parser as pr
from rosbag_processor import downloader as dw
from rosbag_processor import uploader as up

from pathlib import Path
import logging
from datetime import date

SOURCE_BUCKET = 'your source bucket'
SOURCE_PREFIX = 'your source prefix'
DESTINATION_BUCKET = 'your destination bucket'

LOCAL_BAG_FILES_PATH = '/data1/s3/bg1'
LOCAL_PICTURES_DESTINATION = '/data1/s3/pictures1'
TOPICS = ['/realsense_gripper/aligned_depth_to_color/image_raw', '/realsense_gripper/color/image_raw/compressed']
MIN_FILTER_TIME = '2023-08-22 18:33:48'
MAX_FILTER_TIME = '2023-08-22 18:33:52'

APP_FOLDER = '.rosbag_processor'

DEBUG_MODE = True

source_bucket = SOURCE_BUCKET
source_prefix = SOURCE_PREFIX
if not source_prefix[-1] == '/':
    source_prefix += '/'
destination_bucket = DESTINATION_BUCKET

path_to_bag_files = LOCAL_BAG_FILES_PATH
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

    for key, result in dw.download_parallel_multithreading(source_bucket, source_prefix, path_to_bag_files,
                                                           debug_mode=DEBUG_MODE):
        logger.info(f"{key['Key']}, Size = {key['Size']}, result: {result}")
        if DEBUG_MODE:
            print(f"{key['Key']}, Size = {key['Size']}, result: {result}")

    pr.pars_files(path_to_bag_files, path_to_pictures, topics=TOPICS,
                  start_time=MIN_FILTER_TIME, end_time=MAX_FILTER_TIME, debug_mode=DEBUG_MODE)

    up.store_files_to_s3(path_to_pictures, destination_bucket, debug_mode=DEBUG_MODE)

    logger.info("Routine finished")


if __name__ == "__main__":
    start_routine()


