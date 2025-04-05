import boto3
import os

BUCKET_NAME = "cyberorbit"
# s3 = boto3.client("s3")

def sync_down(file_path):
    try:
        s3.download_file(BUCKET_NAME, file_path, file_path)
    except Exception:
        pass

def sync_up(file_path):
    try:
        s3.upload_file(file_path, BUCKET_NAME, file_path)
    except Exception:
        pass