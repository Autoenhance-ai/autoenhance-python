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

        :param image_id: string id of the image

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

        :param img_name: string name of the image house.jpg or house.png
        :param img_path: string name of the image base_dir/house.jpg or image url

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

    def preview_enhanced_img(self, image_id):

        """
        When an image has finished processing, you can view a preview of the image with

        :param image_id: id of the uploaded image

        :return: {'image': <_io.BytesIO object at 0x10363b0e0>, 'status': 200}


        """

        response = self.send_request(method='GET', endpoint=f'image/{image_id}/preview')

        if response.status_code == 200:
            return {'image': io.BytesIO(response.content), 'status': response.status_code}

        return {'error': response.json(), 'status': response.status_code}

    def web_optimised_img(self, image_id):

        """

        Web optimised enhancement.
        Get processed result of uploaded image in different sizes or by default small.


        :param image_id: string id of the uploaded image

        :return: {'image': <_io.BytesIO object at 0x10363b0e0>, 'status': 200}


        """

        response = self.send_request(method='GET', endpoint=f'image/{image_id}/enhanced', params={'size': 'small'})

        if response.status_code == 200:
            return {'image': io.BytesIO(response.content), 'status': response.status_code}

        return {'error': response.json(), 'status': response.status_code}

    def full_resol_enhanced_img(self, image_id):

        """

       The images are usually around 4-6Mb, which can take a long time to load on slow internet.


        :param image_id: string id of the uploaded image

        :return: {'image': <_io.BytesIO object at 0x10363b0e0>, 'status': 200}


        """

        response = self.send_request(method='GET', endpoint=f'image/{image_id}/enhanced')

        if response.status_code == 200:
            return {'image': io.BytesIO(response.content), 'status': response.status_code}

        return {'error': response.json(), 'status': response.status_code}

    def edit_enhanced_img(self, image_id,
                          vertical_correction=True,
                          sky_replacement=True,
                          sky_type='UK_SUMMER',
                          cloud_type='HIGH_CLOUD',
                          contrast_boost='LOW',
                          three_sixty=False):

        """

        If the image should have a sky replacement,
        and it hasn’t been achieved by the AI,
        then you can set sky_replacement: true,
        and the AI will apply a sky replacement to the image.
        If the image shouldn’t have a sky
        replacement, but the AI has applied one,
        then you can set sky_replacement: false,
        to disable the sky replacement.


        :param image_id: string id of the uploaded image
        :param vertical_correction: boolean True to enable perspective correction and false to disable.
        :param sky_replacement: boolean When true the AI will try to replace the sky if it detects a sky in the image.
                                When false the AI will not try to detect or replace the sky in the image.
        :param sky_type: string Set specific sky type. (Options: UK_SUMMER, UK_WINTER or USA_SUMMER). Default is UK_SUMMER.
        :param cloud_type: string Set specific cloud type. (Options: CLEAR, LOW_CLOUD or HIGH_CLOUD). Default is HIGH_CLOUD.
        :param contrast_boost: string Set contrast boost level. (Options: NONE, LOW, MEDIUM or HIGH). Default is LOW
        :param three_sixty: boolean Enable/Disable 360 enhancement. By default, this is false. 360 enhancement requires a 360 panorama.




        :return: {'image': <_io.BytesIO object at 0x10363b0e0>, 'status': 200}


        """

        body = {
            'vertical_correction': vertical_correction,
            'sky_replacement': sky_replacement,
            'sky_type': sky_type,
            'cloud_type': cloud_type,
            'contrast_boost': contrast_boost,
            'threesixty': three_sixty

        }

        response = self.send_request(
            method='POST',
            endpoint=f'image/{image_id}/process',
            json=body)

        if response.status_code == 200:
            return {'image': io.BytesIO(response.content), 'status': response.status_code}

        return {'error': response.json(), 'status': response.status_code}
