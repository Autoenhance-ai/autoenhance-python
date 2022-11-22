import time


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
