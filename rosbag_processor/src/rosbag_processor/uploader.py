import os
import boto3
import botocore
##############################################
# for package build:
from rosbag_processor import settings as st
from rosbag_processor.logger import Logger

# for local testing:
# from logger import Logger
# import settings as st
##############################################

s3_url = st.s3_url
s3_accessKey = st.s3_accessKey
s3_secretKey = st.s3_secretKey
s3_api = st.s3_api
s3_path = st.s3_path
log_file = st.log_file
logger = Logger('uploader_logger', log_file).get()


def store_files_to_s3(path_to_pictures, destination_bucket, debug_mode=False):
    logger.info(f"Storing files to s3 started")
    if debug_mode:
        print(f"Storing files to s3 started")

    b3_session = boto3.Session(aws_access_key_id=s3_accessKey,
                               aws_secret_access_key=s3_secretKey)

    b3_client = b3_session.client('s3',
                                  endpoint_url=s3_url,
                                  config=botocore.client.Config(signature_version=s3_api))

    b3_resource = b3_session.resource('s3',
                                      endpoint_url=s3_url,
                                      config=botocore.client.Config(signature_version=s3_api))

    bucket = b3_resource.Bucket(destination_bucket)

    bucket.objects.all().delete()

    num_files = 0
    for root, sub_dirs, files in os.walk(path_to_pictures):
        if files:
            for file in files:
                file_to_store = os.path.join(root, file)
                object_to_store = file_to_store.replace(path_to_pictures, '')[1:]

                if upload_file_to_s3(b3_client, file_to_store, destination_bucket, object_to_store):
                    num_files += 1
                    logger.info(f"File {file} stored")
                    if debug_mode:
                        print(f"File {file} stored")

    logger.info(f'Stored {num_files} files')
    if debug_mode:
        print(f'Stored {num_files} files')


def upload_file_to_s3(b3_client, file_name, bucket, object_name=None, args=None):
    if object_name is None:
        object_name = file_name

    try:
        response = b3_client.upload_file(file_name, bucket, object_name, ExtraArgs=args)
    except botocore.exceptions.ClientError as error:
        logger.error(error)
        return False

    return True
