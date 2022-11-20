import re
import time
from urllib.request import urlopen


def image_to_buffer(path):
    url = re.findall("(?P<url>https?://[^\s]+)", path)
    if len(url) > 0:
        image_buffer = urlopen(url[0]).read()
    else:
        with open(path, 'rb') as f:
            image_buffer = f.read()

    return image_buffer


def img_type(img_name):
    image_type = img_name.split('.').pop()

    if image_type == 'jpg':
        image_type = 'jpeg'

    return image_type


def get_image_status(put, get_img_status, image_id):
    status = True
    time_out = 0
    if put.status_code == 200:
        while status:
            time_out += 1
            get_status = get_img_status(image_id=image_id)['status']
            if get_status != 'processed':
                time.sleep(5)
            else:
                status = False
            if time_out == 10:
                break

    return {'status': status, 'error': put.content}


def is_correct_response(response):
    return response['status'] == 'processed'
