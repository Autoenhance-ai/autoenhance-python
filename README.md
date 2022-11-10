# The library of Autoenhance.

### Installation

```
pip install auto_anhance

```

### Get started

bla bla bal

### how to work with API

```Python
from auto_enhance import AutoEnhance

auto_enhance = AutoEnhance(auth_key='sHNNOt63uj5DgxPujNZFr3jIgv1CkVW72X3UZHn2')

get_status = auto_enhance.get_img_status(image_id='52ceddc6-1940-485a-98bf-2d122e71806c')

url = 'https://media.istockphoto.com/id/833470744/photo/silhouette-of-lonely-tree.jpg?s=612x612&w=is&k=20&c=KO_gQuPJkpUmyQD-6GjS_3N-Uo5f_yD_gKk4OHoMnxs='
img_path = '/base_dir/image.jpg'

upload = auto_enhance.upload_img(img_name='image.jpg',
                                 img_path=img_path)

```
