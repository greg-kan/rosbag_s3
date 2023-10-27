import os
from pathlib import PurePath
import boto3
import botocore
from concurrent import futures
from concurrent.futures import ThreadPoolExecutor

##############################################
# for package build:
from rosbag_processor import settings as st
from rosbag_processor.logger import Logger

# for local testing:
# from logger import Logger
# import settings as st
##############################################

bag_file_extension = st.bag_file_extension

s3_url = st.s3_url
s3_accessKey = st.s3_accessKey
s3_secretKey = st.s3_secretKey
s3_api = st.s3_api
s3_path = st.s3_path
log_file = st.log_file
logger = Logger('downloader_logger', log_file).get()


def download_parallel_multithreading(source_bucket, source_prefix, path_to_bag_files, debug_mode=False):

    if debug_mode:
        print(f'Downloading files from source_bucket = {source_bucket}, source_prefix = {source_prefix}')
    logger.info(f'Downloading files from source_bucket = {source_bucket}, source_prefix = {source_prefix}')

    if not os.path.exists(path_to_bag_files):
        os.makedirs(path_to_bag_files)
        if debug_mode:
            print(f'Directory created: {path_to_bag_files}')
        logger.info(f'Directory created: {path_to_bag_files}')

    b3_session = boto3.Session(aws_access_key_id=s3_accessKey,
                               aws_secret_access_key=s3_secretKey)  # ,region_name='us-east-1'

    b3_client = b3_session.client('s3',
                                  endpoint_url=s3_url,
                                  config=botocore.client.Config(signature_version=s3_api))

    obj_list = b3_client.list_objects_v2(Bucket=source_bucket, Prefix=source_prefix)

    with ThreadPoolExecutor(max_workers=8) as executor:
        future_to_key = {executor.submit(download_object,
                                         debug_mode,
                                         b3_client,
                                         source_bucket,
                                         path_to_bag_files,
                                         obj['Key']): obj for obj in obj_list['Contents']
                         if get_file_extension(obj['Key']) == bag_file_extension
                         }

        for future in futures.as_completed(future_to_key):
            var_key = future_to_key[future]
            exception = future.exception()

            if not exception:
                yield var_key, future.result()
            else:
                yield var_key, exception


def download_object(debug_mode, s3_client, source_bucket, path_to_bag_files, file_name):  # , debug_mode
    name_file = file_name.split('/', 1)[1]
    download_path = PurePath(path_to_bag_files, name_file)

    logger.info(f"Downloading {file_name} to {download_path}")
    if debug_mode:
        print(f"Downloading {file_name} to {download_path}")

    s3_client.download_file(
        source_bucket,
        file_name,
        str(download_path)
    )

    return "Success"


def get_file_extension(file_name):
    _, f_extension = os.path.splitext(file_name)
    return f_extension.lower()
