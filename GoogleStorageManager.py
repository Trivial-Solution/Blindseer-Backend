import time
from google.cloud import storage
import os
import datetime


class GoogleStorageManager:
    def __init__(self, credentials_file, bucket_name):
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_file
        self.storage_client = storage.Client()
        self.bucket_name = bucket_name
        self.start_time = datetime.datetime.now()
        self.last_checked = set()

    def check_new_images(self, check_interval=1):
        """Check for new images in the bucket every `check_interval` seconds."""
        print(f"Checking for new images in bucket '{self.bucket_name}' every {check_interval} second(s).")

        while True:
            current_blobs = self.__list_blobs()
            new_images = current_blobs - self.last_checked
            most_recent_image = None
            most_recent_time = self.start_time
            most_recent_image_path = None

            for image in new_images:
                filename_without_extension = image.split('.')[0]
                try:
                    image_time = datetime.datetime.strptime(filename_without_extension, "%Y-%m-%d-%H-%M-%S")
                    if image_time > most_recent_time:
                        most_recent_time = image_time
                        most_recent_image = image
                except ValueError:
                    pass  # Ignore files that don't match the expected format

            if most_recent_image:
                print(f"Most recent image found: {most_recent_image}")
                most_recent_image_path = f"images/{most_recent_image}"
                self.__download_blob(most_recent_image, most_recent_image_path)

            self.last_checked = current_blobs

            if most_recent_image_path:
                return most_recent_image_path

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
