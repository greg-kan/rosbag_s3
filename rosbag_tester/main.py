import os
from rosbag_processor import downloader as dw
from rosbag_processor import parser as pr

SOURCE_BAG = '/data1/s3'
SOURCE_PREFIX = 'bg/'
PICTURES_DESTINATION = '/data1/s3/pictures1'
TOPICS = ['/realsense_gripper/aligned_depth_to_color/image_raw', '/realsense_gripper/color/image_raw/compressed']
MIN_FILTER_TIME = '2023-08-22 18:33:48'
MAX_FILTER_TIME = '2023-08-22 18:33:52'

path_to_files = os.path.join(SOURCE_BAG, SOURCE_PREFIX)
path_to_pictures = PICTURES_DESTINATION


def start_routine():
    dw.download_files()
    pr.pars_files(path_to_files, path_to_pictures, topics=TOPICS,
                  start_time=MIN_FILTER_TIME, end_time=MAX_FILTER_TIME)


if __name__ == "__main__":
    start_routine()
