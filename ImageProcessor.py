import json
import time
import requests
import base64
import json


class ImageProcessor:
    def __init__(self, base_uri):
        self.base_uri = base_uri
        self.stream = True
        with open("prompts.json", 'r') as file:
            self.prompts = json.load(file)

    def process_image(self, image_name, gesture):
        if gesture == None:
            gesture = "None"

        payload = {
            'model_path': 'liuhaotian/llava-v1.5-7b',
            'image_base64': ImageProcessor.__encode_image_to_base64(image_name),
            'prompt': self.prompts[gesture],
            'temperature': 0.2,
            'max_new_tokens': 512,
            'stream': self.stream
        }

        timer = Timer()

        r = requests.post(
            f'{self.base_uri}/inference',
            json=payload,
            stream=self.stream,
        )

        print(f'Status code: {r.status_code}')
        response_text = ""

        if self.stream:
            if r.encoding is None:
                r.encoding = 'utf-8'

            for line in r.iter_lines(decode_unicode=True):
                if line:
                    try:
                        line_json = json.loads(line)
                        response_text += line_json.get('response', '') + "\n"
                    except json.JSONDecodeError:
                        pass  # Handle JSON decode error

            time_taken = timer.get_elapsed_time()
        else:
            time_taken = timer.get_elapsed_time()
            resp_json = r.json()
            response_text = resp_json.get('response', '')

        print(f'Total time taken for API call {time_taken} seconds')

        return response_text

    @staticmethod
    def __encode_image_to_base64(image_path):
        with open(image_path, 'rb') as image_file:
            return str(base64.b64encode(image_file.read()).decode('utf-8'))


class Timer:
    def __init__(self):
        self.start = time.time()

    def restart(self):
        self.start = time.time()

    def get_elapsed_time(self):
        end = time.time()
        return round(end - self.start, 1)
