import time
from google.cloud import storage
import os
import datetime


class GoogleStorageManager():
    def __init__(self, credentials_file, bucket_name):
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_file
        self.storage_client = storage.Client()
        self.bucket_name = bucket_name
        self.start_time = datetime.datetime.now()

    def check_new_images(self, check_interval=1):
        """Check for new images in the bucket every `check_interval` seconds."""
        print(f"Checking for new images in bucket '{self.bucket_name}' every {check_interval} second(s).")

        last_checked = set()

        while True:
            current_blobs = self.__list_blobs()
            new_images = current_blobs - last_checked

            for image in new_images:
                # Remove the file extension
                filename_without_extension = image.split('.')[0]
                try:
                    # Parse the datetime from the filename
                    image_time = datetime.datetime.strptime(filename_without_extension, "%Y-%m-%d-%H-%M-%S")
                    if image_time > self.start_time:
                        print(f"New image found: {image}")
                        self.__download_blob(image, f"images/{image}")
                except ValueError:
                    pass  # Ignore files that don't match the expected format

            last_checked = current_blobs
            time.sleep(check_interval)

    def __list_blobs(self):
        """Lists all the blobs in the bucket."""
        storage_client = storage.Client()
        blobs = storage_client.list_blobs(self.bucket_name)
        return set(blob.name for blob in blobs)

    def __download_blob(self, source_blob_name, destination_file_name):
        """Downloads a blob from the bucket."""
        storage_client = storage.Client()
        bucket = storage_client.bucket(self.bucket_name)
        blob = bucket.blob(source_blob_name)

        print(f"Downloading {source_blob_name}")

        blob.download_to_filename(destination_file_name)

        print(f"Blob {source_blob_name} downloaded to {destination_file_name}.")
