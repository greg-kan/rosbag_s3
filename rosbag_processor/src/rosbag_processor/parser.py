import os
from datetime import datetime
from datetime import timezone
import rospy
import rosbag
import cv2
from rosbags.image import message_to_cvimage
from rosbags.image import compressed_image_to_cvimage

##############################################
# for package build:
from rosbag_processor import settings as st
from rosbag_processor.logger import Logger

#  for local testing:
# import settings as st
# from logger import Logger
##############################################

DATA_TYPES = ['sensor_msgs/Image', 'sensor_msgs/CompressedImage']  # Hardcoded according to the task

bag_file_extension = st.bag_file_extension
log_file = st.log_file
logger = Logger('parser_logger', log_file).get()


def pars_files(path_to_files, path_to_pictures, topics=None, start_time=None, end_time=None, debug_mode=False):
    logger.info(f"Processing bag files started with: Local path to files={path_to_files}, "
                f"Topics={topics}, Start time={start_time}, End time={end_time}")

    epoch_start = '1980-01-01'
    epoch_end = '2900-12-31'

    if start_time is None:
        start_time_t = datetime.strptime(epoch_start, '%Y-%m-%d')
    else:
        start_time_t = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')

    if end_time is None:
        end_time_t = datetime.strptime(epoch_end, '%Y-%m-%d')
    else:
        end_time_t = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')

    start_timestamp = rospy.Time.from_sec(start_time_t.replace(tzinfo=timezone.utc).timestamp())
    end_timestamp = rospy.Time.from_sec(end_time_t.replace(tzinfo=timezone.utc).timestamp())

    if start_timestamp > end_timestamp:
        logger.error(f"Start filter time={start_time} is greater than End filter time={end_time}")

        if debug_mode:
            print('Error: End filter time is greater than Start filter time')
        return

    lst_files = os.listdir(path_to_files)
    lst_files = sorted([os.path.join(path_to_files, fl)
                       for fl in lst_files if get_file_extension(fl) == bag_file_extension])

    if debug_mode:
        print(f'start_timestamp = {start_timestamp}, end_timestamp = {end_timestamp}')

    for fl in lst_files:
        process_bag_file(fl, path_to_pictures, topics, start_timestamp, end_timestamp, debug_mode)


def process_bag_file(file_name, path_to_pictures, topics, start_time, end_time, debug_mode):
    logger.info(f"Processing file: {file_name}")
    if debug_mode:
        print(f"Processing file: {file_name}")

    folder_name_suffix_start = datetime.utcfromtimestamp(int(start_time.secs)).strftime('%Y-%m-%d_%H-%M-%S')
    folder_name_suffix_end = datetime.utcfromtimestamp(int(end_time.secs)).strftime('%Y-%m-%d_%H-%M-%S')
    folder_name_suffix = folder_name_suffix_start + '_' + folder_name_suffix_end

    bag = rosbag.Bag(file_name, 'r')

    for topic, msg, t in bag.read_messages(topics=topics, start_time=start_time, end_time=end_time,
                                           connection_filter=filter_image_msgs):
        datatype = (str(type(msg)).split('__')[1])[:-2]
        process_bag_message(file_name, path_to_pictures, topic, msg, datatype, t, folder_name_suffix, debug_mode)

    bag.close()


def process_bag_message(file_name, path_to_pictures, topic, message, datatype, time_stamp,
                        folder_name_suffix, debug_mode):
    base_file_name = get_file_name(os.path.basename(file_name))

    nanosecs = str(time_stamp.nsecs)
    time_str = datetime.utcfromtimestamp(int(time_stamp.secs)).strftime('%Y-%m-%d_%H-%M-%S') + '-' + nanosecs

    out_file_name = time_str + '(' + base_file_name + ')'
    topic_str = topic[1:].replace('/', '_')

    out_dir_name = os.path.join(path_to_pictures, topic_str, datatype, folder_name_suffix, '')

    img = None
    if datatype == 'Image':
        img = message_to_cvimage(message)
    elif datatype == 'CompressedImage':
        img = compressed_image_to_cvimage(message)

    if not os.path.exists(out_dir_name):
        os.makedirs(out_dir_name)

    if img is not None:
        cv2.imwrite(out_dir_name + out_file_name + '.png', img)
        logger.info(f"Written file: {out_file_name}")

    if debug_mode:
        print(f"Written file: {out_file_name}")


def filter_image_msgs(topic, datatype, md5sum, msg_def, header):
    if datatype in DATA_TYPES:
        return True

    return False


def get_file_name(file_name):
    f_name, _ = os.path.splitext(file_name)
    return f_name.lower()


def get_file_extension(file_name):
    _, f_extension = os.path.splitext(file_name)
    return f_extension.lower()
