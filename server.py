from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Endpoint to upload images
@app.route('/upload', methods=['POST'])
def upload_image():
    # Check if an image was uploaded
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400

    # Get the uploaded image
    image = request.files['image']
    image.save("test_2.png")

    return jsonify({'message': 'Image uploaded successfully'}), 200

# Sends the text to the Flutter App
def send_text(text: str):
    api_url = 'https://external-api.example.com/endpoint'

    # Send the text data to the external API
    response = requests.post(api_url, data={'text': text})

    # Check if the request to the external API was successful
    response.raise_for_status()  # This will raise an HTTPError if the HTTP request returned an unsuccessful status code

    return response.json()

if __name__ == '__main__':
    app.run(debug=True)
