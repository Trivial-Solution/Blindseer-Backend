# Replace with your Google Cloud Storage bucket name
import time

from DockerService import DockerService
from FirestoreManager import FirestoreManager
from GoogleStorageManager import GoogleStorageManager
from ImageProcessor import ImageProcessor


def main():
    firestore_manager = FirestoreManager('keys/blindseer-cfefc-firebase-adminsdk-h2tky-d80b878c18.json')
    google_storage_manager = GoogleStorageManager('keys/skilled-mission-405818-0b879b4080fd.json', 'blindseer-images')
    image_processor = ImageProcessor('http://127.0.0.1:5000')

    DockerService.start_docker()
    time.sleep(5)

    while True:
        most_recent_image_path = google_storage_manager.check_new_images()

        if most_recent_image_path:
            # Process the most recent image
            processed_result = image_processor.process_image(most_recent_image_path)
            # Handle the processed image as needed
            print(f"Processed image with text: {processed_result}")
            firestore_manager.upload_text(processed_result)
            print(f'Uploaded text to Firestore')


if __name__ == "__main__":
    main()
