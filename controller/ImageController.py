import os

import controller.Util
from module.Image import Image


def _generate_image_name(danbooru, indx, url):
    dump, extension = os.path.splitext(url)
    image_name = danbooru.get_tags() + " " + str(indx) + extension
    return image_name


def download_image(danbooru, indx, url, path, log_box):
    image_name = _generate_image_name(danbooru, indx, url)
    image = Image(image_name, url)
    res = image.download(path)
    if not res[0]:
        controller.Util.insert_log(log_box, res[1], 'warning')
