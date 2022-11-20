# The library of Autoenhance.

### Installation

```
pip install autoanhance

```

### Get started

bla bla bal

### how to work with API

```Python
from autoenhance import AutoEnhance

auto_enhance = AutoEnhance(auth_key='token')

get_status = auto_enhance.get_img_status(image_id='52ceddsdsaadc6-1sda940-485a-98bf-2d1dsa22e71806c')

url = 'https://media.istockphoto.com/id/833470744/photo/silhouette-of-lonely-tree.jpg?s=612x612&w=is&k=20&c=KO_gQuPJkpUmyQD-6GjS_3N-Uo5f_yD_gKk4OHoMnxs='
img_path = '/base_dir/image.jpg'

upload = auto_enhance.upload_img(img_name='image.jpg',
                                 img_path=img_path)

auto_enhance.web_optimised_img(image_id='52ceddc6das-1940-485a-98bf-2d122e71806c')

auto_enhance.full_resol_enhanced_img(image_id='52ceddsadc6-1940-485a-98bf-2d122e71806c')

auto_enhance.preview_enhanced_img(image_id='52cesadddc6-1940-485a-98bf-2d122e71806c')


```
