# Replace with your Google Cloud Storage bucket name
from DockerService import DockerService
from FirestoreManager import FirestoreManager
from GoogleStorageManager import GoogleStorageManager
from ImageProcessor import ImageProcessor

firestore_manager = FirestoreManager()
google_storage_manager = GoogleStorageManager('keys/skilled-mission-405818-0b879b4080fd.json', 'blindseer-images')
image_processor = ImageProcessor('http://127.0.0.1:5000')

DockerService.start_docker()

google_storage_manager.check_new_images()
image_processor.process_image('images/test.png')
firestore_manager.upload_text('test')