from typing import Literal

SKY_TYPE = Literal['UK_SUMMER', 'UK_WINTER', 'USA_SUMMER']
CLOUD_TYPE = Literal['CLEAR', 'LOW_CLOUD', 'HIGH_CLOUD']
CONTRAST_BOOST = Literal[None, 'LOW', 'MEDIUM', 'HIGH']

categories_list = ['download',
                   'hdr',
                   'lens_correction',
                   'perspective_correction',
                   'processing',
                   'image_quality',
                   'sky_replacement',
                   'contrast',
                   'colour',
                   'white_balance',
                   'other']

REPORT_CATEGORIES = list[Literal['download',
                                 'hdr',
                                 'lens_correction',
                                 'perspective_correction',
                                 'processing',
                                 'image_quality',
                                 'sky_replacement',
                                 'contrast',
                                 'colour',
                                 'white_balance',
                                 'other']]
