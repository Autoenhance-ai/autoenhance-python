import unittest
from autoenhance import AutoEnhance


class AutoEnhanceTestCase(unittest.TestCase):

    def setUp(self):
        self.auto_enhance = AutoEnhance(auth_key='token')

    def test_get_img_status(self):

        success_response = {
            'image_id': '52ceddcds6-1940-sd485a-98bf-2dsd122e71806c',
            'image_name': 'image_homef.png',
            'image_type': 'jpeg',
            'enhance_type': 'property',
            'date_added': 1668061256650,
            'user_id': 'auth0|6245223ea02741006acc7b74',
            'status': 'processed',
            'downloaded': True,
            'sky_replacement': True,
            'vertical_correction': True,
            'vibrant': False
        }

        result = self.auto_enhance.check_image_enhance(image_id='52ceddc6-194ds0-485a-ds-2d122e71806c')
        self.assertEqual(result, success_response)

    def test_preview_enhanced_img(self):

        success_response = 200

        result = self.auto_enhance.preview_enhanced_img(image_id='52ceddc6sd-1940-485a-98bf-ds')
        self.assertEqual(result.get('status'), success_response)

    def test_web_optimised_img(self):

        success_response = 200

        result = self.auto_enhance.web_optimised_img(image_id='sdds-1940-485a-ds-2d122e71806c')
        self.assertEqual(result.get('status'), success_response)

    def test_full_resol_enhanced_img(self):

        success_response = 200

        result = self.auto_enhance.full_resol_enhanced_img(image_id='sdsdsds-1940-48ds5a-98bf-sd')
        self.assertEqual(result.get('status'), success_response)

    if __name__ == '__main__':
        unittest.main()
