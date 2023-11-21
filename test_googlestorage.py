import time
from google.cloud import storage
import os

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'keys/skilled-mission-405818-0b879b4080fd.json'


def list_blobs(bucket_name):
    """Lists all the blobs in the bucket."""
    storage_client = storage.Client()
    blobs = storage_client.list_blobs(bucket_name)

    return set(blob.name for blob in blobs)


def check_new_images(bucket_name, check_interval=1):
    """Check for new images in the bucket every `check_interval` seconds."""
    print(f"Checking for new images in bucket '{bucket_name}' every {check_interval} second(s).")

    last_checked = set()

    while True:
        current_blobs = list_blobs(bucket_name)
        new_images = current_blobs - last_checked

        if new_images:
            print(f"New image(s) found: {new_images}")

        last_checked = current_blobs
        time.sleep(check_interval)

def download_blob(bucket_name, source_blob_name, destination_file_name):
    """Downloads a blob from the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(source_blob_name)

    print(f"Downloading {source_blob_name}")

    blob.download_to_filename(destination_file_name)

    print(f"Blob {source_blob_name} downloaded to {destination_file_name}.")


# Replace with your Google Cloud Storage bucket name
bucket_name = 'blindseer-images'

#check_new_images(bucket_name)

download_blob(bucket_name, 'spronk.png', 'spronk.png')