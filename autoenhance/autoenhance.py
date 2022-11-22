import io
from mimetypes import guess_type
from typing import Optional

import polling2
import requests
from requests import Request, Session
from requests.adapters import HTTPAdapter, Retry

from helpers.helper import is_correct_response
from helpers.param_types import CONTRAST_BOOST, SKY_TYPE, CLOUD_TYPE, categories_list, REPORT_CATEGORIES


class AutoEnhance:
    auth_key: ''
    BASE_URL = 'https://api.autoenhance.ai/v2/'

    def __init__(self, auth_key):
        self.auth_key = auth_key

    def send_request(self, endpoint, method, json=None, params=None):
        request = Request(method=method, url=self.BASE_URL + endpoint)

        if json:
            request.json = json

        if params:
            request.params = params

        prep = request.prepare()

        prep.headers['x-api-key'] = self.auth_key

        session = Session()

        retries = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504])
        session.mount(self.BASE_URL + endpoint, HTTPAdapter(max_retries=retries))

        response = session.send(prep)
        return response

    def upload_img(self,
                   img_name: str,
                   image_buffer: bytes,
                   order_id: Optional[str] = None,
                   enhance_type: Optional[str] = None,
                   vertical_correction: Optional[bool] = True,
                   sky_replacement: Optional[bool] = True,
                   sky_type: SKY_TYPE = 'UK_SUMMER',
                   cloud_type: CLOUD_TYPE = 'HIGH_CLOUD',
                   contrast_boost: CONTRAST_BOOST = 'LOW',
                   threesixty: Optional[bool] = False,
                   hdr: Optional[bool] = False,
                   ):

        # https://api.autoenhance.ai/v2/image
        """

        Upload an image and get image id or order id by which you can get processed image.

        :param img_name: name of the image house.jpg or house.png
        :param image_buffer: pass image as a buffer
        :param order_id: UUID string to link a group of images under one order (e.g. b1aa3999-7908-45c9-9a99-82e25cf5de8e).
        :param enhance_type: Type of image you want enhanced (e.g. property or food).
        :param vertical_correction: Enable/Disable vertical correction. By default, this is true.
        :param sky_replacement: Enable/Disable sky replacement. By default, this is true.
        :param sky_type: Set specific sky type. (Options: UK_SUMMER, UK_WINTER or USA_SUMMER). Default is UK_SUMMER.
        :param cloud_type: Set specific cloud type. (Options: CLEAR, LOW_CLOUD or HIGH_CLOUD). Default is HIGH_CLOUD.
        :param contrast_boost: Set contrast boost level. (Options: NONE, LOW, MEDIUM or HIGH). Default is LOW.
        :param threesixty: Enable/Disable 360 enhancement. By default, this is false. 360 enhancement requires a 360 panorama.
        :param hdr: Enable/Disable HDR. By default, this is false.
                    HDR will require multiple brackets, and an additional API call. Read more on how to enhance HDR.

        :return: {'image_id': 'i13221-dsadar-fdsf', 'order_id': 'dsadsadas2e3124', 'status': 200}


        """
        image_type = guess_type(img_name)[0]

        body = {
            'image_name': img_name,
            'content_type': image_type,
            'order_id': order_id,
            'enhance_type': enhance_type,
            'vertical_correction': vertical_correction,
            'sky_replacement': sky_replacement,
            'sky_type': sky_type,
            'cloud_type': cloud_type,
            'contrast_boost': contrast_boost,
            'threesixty': threesixty,
            'hdr': hdr,
        }

        post = self.send_request(method='POST', endpoint='image', json=body)

        if post.status_code == 200:

            image_url = post.json().get('s3PutObjectUrl')
            image_id = post.json().get('image_id')

            put = requests.put(url=image_url, data=image_buffer,
                               headers={'Content-Type': image_type})

            if put.status_code == 200:
                response = {'image_id': image_id, 'order_id': body.get('order_id'), 'status': put.status_code}
                return response

            return {'message': put.content, 'status': put.status_code}
        return {'message': post.content, 'status': post.status_code}

    def check_image_enhance(self,
                            image_id: str,
                            polling: Optional[bool] = False):

        # https://api.autoenhance.ai/v2/image/:image_id

        """

        Check image status by image id.

        :param image_id: string id of the image
        :param polling: if polling then set it to True

        :return: {'image_id': '8210c1asdsa42-02a0-4692dfs-a2aa-e704e8dfdsfad04e',
                'image_name': 'house.jpg',
                'image_type': 'jpeg',
                'enhance_type': 'property',
                'date_added': 334213214325,
                'user_id': 'auth0|342rfef43rfds',
                'status': 'processing'}

        """
        if polling:
            response = polling2.poll(
                lambda: self.send_request(method='GET', endpoint=f'image/{image_id}').json(),
                check_success=is_correct_response,
                step=1.5,
                max_tries=10,
                timeout=20)

            return response

        return self.send_request(method='GET', endpoint=f'image/{image_id}').json()

    def check_order_enhance(self, order_id: str):

        # https://api.autoenhance.ai/v2/order/:order_id

        """

        Check images status by order id.

        :param order_id: string id of the order

        :return: {'images': [{'image_id': '098c8f40-b3bd-4301-98eb-2a51be989dac', 'order_id': '3212310-dfs-fdsg0',
        'image_name': 'image.jpg', 'image_type': 'jpeg', 'enhance_type': 'property', 'date_added': 1669056195000,
        'user_id': 'auth0|6363dbcb77f7e74122ea6350', 'status': 'processed', 'sky_replacement': True,
        'vertical_correction': True, 'vibrant': False},

         {'image_id': 'd19d9cfa-dccf-466c-a2cf-8df761317db3', 'order_id': '3212310-dfs-fdsg0',
         'image_name': 'image.jpg', 'image_type': 'jpeg', 'enhance_type': 'property', 'date_added': 1669056341000,
          'user_id': 'auth0|6363dbcb77f7e74122ea6350', 'status': 'processed', 'sky_replacement': True,
          'vertical_correction': True, 'vibrant': False}], 'is_processing': False, 'order_id': '3212310-dfs-fdsg0'}

        """

        return self.send_request(method='GET', endpoint=f'order/{order_id}').json()

    def preview_enhanced_img(self, image_id: str):

        # https://api.autoenhance.ai/v2/image/:image_id/preview

        """
        When an image has finished processing, you can view a preview of the image with

        :param image_id: id of the uploaded image

        :return: {'image': <_io.BytesIO object at 0x10363b0e0>, 'status': 200}


        """

        response = self.send_request(method='GET', endpoint=f'image/{image_id}/preview')

        if response.status_code == 200:
            return {'image': io.BytesIO(response.content), 'status': response.status_code}

        return {'error': response.json(), 'status': response.status_code}

    def web_optimised_img(self, image_id: str):

        # https://api.autoenhance.ai/v2/image/:image_id}/enhanced?size=small

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

    def full_resol_enhanced_img(self, image_id: str):

        # https://api.autoenhance.ai/v2/image/:image_id/enhanced

        """

       The images are usually around 4-6Mb, which can take a long time to load on slow internet.


        :param image_id: string id of the uploaded image

        :return: {'image': <_io.BytesIO object at 0x10363b0e0>, 'status': 200}


        """

        response = self.send_request(method='GET', endpoint=f'image/{image_id}/enhanced')

        if response.status_code == 200:
            return {'image': io.BytesIO(response.content), 'status': response.status_code}

        return {'error': response.json(), 'status': response.status_code}

    def edit_enhanced_img(self,
                          image_id: str,
                          vertical_correction: Optional[bool] = True,
                          sky_replacement: Optional[bool] = True,
                          sky_type: SKY_TYPE = 'UK_SUMMER',
                          cloud_type: CLOUD_TYPE = 'HIGH_CLOUD',
                          contrast_boost: CONTRAST_BOOST = 'LOW',
                          threesixty: Optional[bool] = False):

        # https://api.autoenhance.ai/v2/image/:image_id/process

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
        :param threesixty: boolean Enable/Disable 360 enhancement. By default, this is false. 360 enhancement requires a 360 panorama.




        :return: {'image': <_io.BytesIO object at 0x10363b0e0>, 'status': 200}


        """

        body = {
            'vertical_correction': vertical_correction,
            'sky_replacement': sky_replacement,
            'sky_type': sky_type,
            'cloud_type': cloud_type,
            'contrast_boost': contrast_boost,
            'threesixty': threesixty

        }

        response = self.send_request(
            method='POST',
            endpoint=f'image/{image_id}/process',
            json=body)

        if response.status_code == 200:
            return {'image': io.BytesIO(response.content), 'status': response.status_code}

        return {'error': response.json(), 'status': response.status_code}

    def report_enhancement(self,
                           image_id: str,
                           category: REPORT_CATEGORIES,
                           comment: Optional[str] = None):

        for i in category:
            if i not in categories_list:
                raise ValueError(f'\"{i}\" is not in  the categories list. Valid values are {categories_list}')

        # https://api.autoenhance.ai/v2/image/:image_id/report
        """

        Current reporting categories:
            download: Image failed to download
            hdr: Images failed to merge properly or be grouped correctly
            lens_correction: Image failed to have lens corrected or incorrectly corrected.
            perspective_correction: Image failed to have perspective corrected or incorrectly corrected.
            processing: The image was stuck in processing and never returned.
            image_quality: The image quality is bad.
            sky_replacement: Image failed to have sky replacement, incorrectly replaced sky or the sky replacement was bad.
            contrast: Too much contrast or not enough contrast.
            colour: The colour is off or not right.
            white_balance: The image is too warm or too cool.
            other: You are reporting the image for a reason not currently within our categories.


        :param image_id: string id of the uploaded image
        :param category: An array of items that the image failed at. e.g. skyreplacement, lenscorrection etc.
                         ["skyreplacement","lenscorrection"]
        :param comment: An optional text comment to provide more infomation about why the image failed.
                                When false the AI will not try to detect or replace the sky in the image.
                                e.g. Sky was not replaced in image and the len has not been corrected


        :return: {'status': 200}


        """

        body = {
            'category': category,
            'comment': comment,

        }

        response = self.send_request(
            method='POST',
            endpoint=f'image/{image_id}/report',
            json=body)

        if response.status_code == 200:
            return {'status': response.status_code}

        return {'status': response.status_code}
