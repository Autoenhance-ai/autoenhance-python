import io
import requests
from requests import Request, Session

from helpers.helper import image_to_buffer, img_type, check_img_status


class AutoEnhance:
    auth_key: ''
    base_url = 'https://api.autoenhance.ai/v2/'

    def __init__(self, auth_key, ):
        self.auth_key = auth_key

    def send_request(self, endpoint, method, json=None, params=None):
        request = Request(method=method, url=self.base_url + endpoint)

        if json:
            request.json = json

        if params:
            request.params = params

        prep = request.prepare()

        prep.headers['x-api-key'] = self.auth_key

        session = Session()
        response = session.send(prep)
        return response

    def get_img_status(self, image_id):

        """

        Check image status.

        :param image_id: id of the image

        :return: {'image_id': '8210c1asdsa42-02a0-4692dfs-a2aa-e704e8dfdsfad04e',
                'image_name': 'house.jpg',
                'image_type': 'jpeg',
                'enhance_type': 'property',
                'date_added': 334213214325,
                'user_id': 'auth0|342rfef43rfds',
                'status': 'processing'}

        """

        response = self.send_request(method='GET', endpoint=f'image/{image_id}').json()

        return response

    def upload_img(self, img_name, img_path):

        """

        Upload an image and get processed result.

        :param img_name: name of the image house.jpg or house.png
        :param img_path: name of the image base_dir/house.jpg or image url

        :return: {'image': <_io.BytesIO object at 0x10363b0e0>, 'status': 200}


        """

        body = {
            'image_name': img_name,
            'content_type': f'image/{img_type(img_name)}'
        }

        post = self.send_request(method='POST', endpoint='image', json=body)
        image_url = post.json().get('s3PutObjectUrl')
        image_id = post.json().get('image_id')

        put = requests.put(url=image_url, data=image_to_buffer(img_path),
                           headers={'Content-Type': f'image/{img_type(img_name)}'})

        status = check_img_status(put, self.get_img_status, image_id)

        if not status.get('status'):
            response = self.send_request(method='GET', endpoint=f'image/{image_id}/preview')

            if response.status_code == 200:
                return {'image': io.BytesIO(response.content), 'status': response.status_code}

            return {'message': response.json(), 'status': response.status_code}

        return status.get('error')

