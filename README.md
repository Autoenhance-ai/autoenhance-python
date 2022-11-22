# The library of Autoenhance.

### Installation

```
pip install autoanhance

```

### Get started

bla bla bal

### Basic usage

```Python
from autoenhance import AutoEnhance

auto_enhance = AutoEnhance(auth_key='token')

upload = auto_enhance.upload_img(img_name='image.jpg',
                                 image_buffer=b'')

check_img_status_by_id = auto_enhance.check_img_status_by_id(
    image_id='52ceddsdsaadc6-1sda940-485a-98bf-2d1dsa22e71806c')

check_img_status_by_order_id = auto_enhance.check_img_status_by_order_id(order_id='52ce71806c')

auto_enhance.preview_enhanced_img(image_id='52cesadddc6-1940-485a-98bf-2d122e71806c')


```
