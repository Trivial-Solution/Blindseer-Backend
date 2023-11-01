import requests


def send_image_to_server(image_path, server_url="http://localhost:5000/upload"):
    """
    Send an image to the specified server URL.

    Parameters:
    - image_path (str): Path to the image file to send.
    - server_url (str): URL of the server to which the image should be sent.

    Returns:
    - dict: Response JSON data from the server.
    """
    with open(image_path, 'rb') as image_file:
        files = {'image': image_file}
        response = requests.post(server_url, files=files)

        # Check if the request was successful
        response.raise_for_status()

        return response.json()


# Example usage:
if __name__ == "__main__":
    image_path = "test.png"
    response_data = send_image_to_server(image_path)
    print(response_data)
